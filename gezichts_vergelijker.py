import face_recognition
import numpy as np

# --- CONFIGURATIE (PADEN AANPASSEN) ---
# PAS DEZE PADEN AAN ZODAT ZE NAAR ECHTE FOTO'S OP JE COMPUTER VERWIJZEN.
# Zorg ervoor dat:
# 1. Elke 'bekende' foto EEN duidelijk gezicht bevat.
# 2. De 'onbekende' foto EEN of MEER gezichten kan bevatten.

AFBEELDING_VAN_JASMIJN = "pad/naar/foto_van_jasmijn.jpg"
AFBEELDING_VAN_ALI = "pad/naar/foto_van_ali.jpg"
ONBEKENDE_AFBEELDING = "pad/naar/onbekende_persoon.jpg"

# Definieer de drempel voor gelijkenis (hogere waarde = soepeler/minder streng)
# 0.6 is een gangbare drempel. Afstand onder deze waarde wordt als 'match' beschouwd.
DREMPEL_GELIJKHEID = 0.6

def codeer_gezicht(bestandspad):
    """Laadt een afbeelding en codeert het gezicht in een unieke numerieke vector."""
    try:
        afbeelding = face_recognition.load_image_file(bestandspad)
        # We nemen aan dat er slechts ÉÉN bekend gezicht in de referentiefoto staat.
        gezichten = face_recognition.face_encodings(afbeelding)
        
        if not gezichten:
            print(f"❌ Geen gezicht gevonden in {bestandspad}. Controleer de foto.")
            return None
            
        return gezichten[0]
    except FileNotFoundError:
        print(f"❌ Bestand niet gevonden: {bestandspad}")
        return None
    except Exception as e:
        print(f"❌ Fout bij verwerking {bestandspad}: {e}")
        return None

def vergelijk_gezichten():
    """Voert de hoofdlogica uit om onbekende gezichten te matchen met bekende gezichten."""
    
    # 1. Bekende Gezichten Coderen
    print("--- Fase 1: Gezichten Coderen ---")
    
    encoding_jasmijn = codeer_gezicht(AFBEELDING_VAN_JASMIJN)
    encoding_ali = codeer_gezicht(AFBEELDING_VAN_ALI)
    
    if encoding_jasmijn is None or encoding_ali is None:
        print("\nKan niet verder. Controleer de paden en foto's van Jasmijn en Ali.")
        return

    # Maak een lijst van de bekende coderingen en hun namen
    bekende_coderingen = [encoding_jasmijn, encoding_ali]
    bekende_namen = ["Jasmijn", "Ali"]
    
    print(f"\n✅ {len(bekende_namen)} bekende gezichten succesvol gecodeerd.")

    # 2. Onbekende Gezichten in de Testafbeelding Coderen
    print("\n--- Fase 2: Onbekende Gezichten Analyseren ---")
    
    onbekende_afbeelding = face_recognition.load_image_file(ONBEKENDE_AFBEELDING)
    onbekende_coderingen = face_recognition.face_encodings(onbekende_afbeelding)

    if not onbekende_coderingen:
        print(f"❌ Geen gezicht gevonden in de onbekende afbeelding: {ONBEKENDE_AFBEELDING}")
        return
        
    print(f"✅ {len(onbekende_coderingen)} gezicht(en) gevonden in de onbekende foto.")

    # 3. Vergelijken en Matchen
    print("\n--- Fase 3: Gezichten Vergelijken ---")

    for i, onbekende_encoding in enumerate(onbekende_coderingen):
        
        # Bereken de Euclidische afstand tussen de onbekende en alle bekende gezichten
        gezichts_afstanden = face_recognition.face_distance(bekende_coderingen, onbekende_encoding)

        # Zoek de kortste afstand (meeste gelijkenis)
        kortste_afstand_index = np.argmin(gezichts_afstanden)
        kortste_afstand = gezichts_afstanden[kortste_afstand_index]
        
        naam = "Onbekend"
        
        if kortste_afstand <= DREMPEL_GELIJKHEID:
            # Er is een match binnen de ingestelde drempel
            naam = bekende_namen[kortste_afstand_index]
            
        print(f"Gezicht {i+1}:")
        print(f"  - Kortste Afstand tot {bekende_namen[kortste_afstand_index]}: {kortste_afstand:.4f}")
        
        if naam != "Onbekend":
            print(f"  ➡️ **MATCH GEVONDEN:** Dit is hoogstwaarschijnlijk **{naam}**!")
        else:
            print(f"  ➡️ **GEEN MATCH:** De gelijkenis is te laag ({kortste_afstand:.4f} > {DREMPEL_GELIJKHEID:.2f}).")
            
        print("-" * 20)

if __name__ == "__main__":
    vergelijk_gezichten()
