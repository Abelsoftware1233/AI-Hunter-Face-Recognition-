import sys
import face_recognition
import numpy as np

# Importeer de database functies uit database_index.py
from database_index import haal_alle_coderingen_op, convert_array, DB_NAAM, sqlite3 

# Drempel voor gelijkenis (deze moet overeenkomen met de drempel in gezichts_vergelijker.py)
DREMPEL_GELIJKHEID = 0.6

def codeer_onbekend_gezicht(bestandspad):
    """Laadt de onbekende afbeelding en haalt de codering van het eerste gezicht op."""
    try:
        afbeelding = face_recognition.load_image_file(bestandspad)
        gezichten = face_recognition.face_encodings(afbeelding)
        
        if not gezichten:
            print(f"❌ Geen gezicht gevonden in de onbekende foto: {bestandspad}")
            return None
            
        print(f"✅ Eerste gezichtscodering van de onbekende foto succesvol gemaakt.")
        return gezichten[0]
        
    except Exception as e:
        print(f"❌ Fout bij het coderen van het onbekende gezicht: {e}")
        return None

def zoek_in_index(onbekende_codering):
    """Vergelijkt de onbekende codering met alle coderingen in de database."""
    
    conn = None
    try:
        # Maak verbinding met de database en gebruik de geregistreerde converters
        conn = sqlite3.connect(DB_NAAM, detect_types=sqlite3.PARSE_DECLTYPES)
        indexed_data = haal_alle_coderingen_op(conn)
        
        if not indexed_data:
            print("⚠️ Database is leeg. Geen vergelijking mogelijk.")
            return "Database Leeg", None, None

        # Scheid de namen, coderingen en URL's in aparte lijsten
        indexed_namen, indexed_coderingen_raw, indexed_urls = zip(*indexed_data)
        
        # Omdat SQLite de coderingen als binaire data opslaat, moeten we ze decoderen
        indexed_coderingen = [convert_array(raw) for raw in indexed_coderingen_raw]
        
        # Bereken de afstand tussen het onbekende gezicht en alle bekende gezichten
        gezichts_afstanden = face_recognition.face_distance(indexed_coderingen, onbekende_codering)

        # Zoek de kortste afstand (meeste gelijkenis)
        kortste_afstand_index = np.argmin(gezichts_afstanden)
        kortste_afstand = gezichts_afstanden[kortste_afstand_index]
        
        beste_naam = indexed_namen[kortste_afstand_index]
        beste_url = indexed_urls[kortste_afstand_index]
        
        if kortste_afstand <= DREMPEL_GELIJKHEID:
            print(f"\n✨ MATCH GEVONDEN in de database! ✨")
            print(f"  - Naam: {beste_naam}")
            print(f"  - Gelijkenis (afstand): {kortste_afstand:.4f}")
            print(f"  - Bron: {beste_url}")
            return beste_naam, kortste_afstand, beste_url
        else:
            print(f"\n❌ GEEN MATCH gevonden in de database binnen de drempel ({DREMPEL_GELIJKHEID}).")
            print(f"  - Beste match was met {beste_naam} op afstand {kortste_afstand:.4f}.")
            return "Geen Match", kortste_afstand, None

    except sqlite3.OperationalError as e:
        print(f"❌ Fout bij databasebewerking: {e}. Zorg ervoor dat 'database_index.py' is uitgevoerd.")
        return "Fout", None, None
    finally:
        if conn:
            conn.close()

# --- Hoofdprogramma Uitvoeren ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python main_runner.py [pad_naar_onbekende_foto.jpg]")
        sys.exit(1)
        
    ONBEKENDE_FOTO_PAD = sys.argv[1]
    
    # 1. Coderen van de Invoerfoto
    onbekende_codering = codeer_onbekend_gezicht(ONBEKENDE_FOTO_PAD)
    
    if onbekende_codering is not None:
        # 2. Zoeken in de Index
        zoek_in_index(onbekende_codering)
        
        # 3. Indien geen match in de database: Vraag of de gebruiker Google wil proberen
        if "Geen Match" in zoek_in_index(onbekende_codering):
             antwoord = input("\nWil je een externe (Google) zoekopdracht starten voor deze afbeelding? (j/n): ")
             if antwoord.lower() == 'j':
                 print("\n➡️ Starten van de externe zoekopdracht via 'zoek_via_google.py'...")
                 # Dit is een simpele manier om het andere script aan te roepen, maar
                 # een directe import van de functie uit zoek_via_google.py is beter in echte code.
                 # Hier gebruiken we de simpele aanroep:
                 # Je zou de functie 'start_reverse_image_search' hier direct moeten importeren
                 # Bijvoorbeeld: from zoek_via_google import start_reverse_image_search
                 # En dan: start_reverse_image_search(ONBEKENDE_FOTO_PAD)
                 # Voor nu vertrouwen we op de instructies van zoek_via_google.py
               
