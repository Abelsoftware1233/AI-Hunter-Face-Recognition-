import os
import face_recognition
import sqlite3

# Importeer de database functies
from database_index import voeg_gezicht_toe, maak_database_tabel, DB_NAAM, sqlite3

# --- CONFIGURATIE (PAD AANPASSEN) ---
MAP_MET_FOTO_INDEX = "pad/naar/jouw/foto_collectie/om_te_indexeren" # VERVANG DIT PAD!
TOEGELATEN_EXTENSIES = ('.jpg', '.jpeg', '.png')

def indexeer_map(map_pad):
    """Codeert alle gezichten in een map en slaat ze op in de database."""
    
    conn = sqlite3.connect(DB_NAAM, detect_types=sqlite3.PARSE_DECLTYPES)
    maak_database_tabel(conn) # Zorg dat de tabel bestaat
    
    totaal_verwerkt = 0
    
    print(f"\n--- Start Indexering van Map: {map_pad} ---")
    
    for bestandsnaam in os.listdir(map_pad):
        if bestandsnaam.lower().endswith(TOEGELATEN_EXTENSIES):
            volledig_pad = os.path.join(map_pad, bestandsnaam)
            
            # De naam voor de database is de bestandsnaam zonder extensie
            naam = os.path.splitext(bestandsnaam)[0]
            
            try:
                afbeelding = face_recognition.load_image_file(volledig_pad)
                gezichten = face_recognition.face_encodings(afbeelding)
                
                if gezichten:
                    # Sla alleen het eerste gevonden gezicht op (als de foto 1 persoon is)
                    voeg_gezicht_toe(conn, naam, gezichten[0], f"Lokaal Bestand: {bestandsnaam}")
                    totaal_verwerkt += 1
                else:
                    print(f"⚠️ Geen gezicht gevonden in {bestandsnaam}. Overslaan.")

            except Exception as e:
                print(f"❌ Fout bij het verwerken van {bestandsnaam}: {e}")
                
    conn.close()
    print(f"\n--- Indexering Voltooid ---")
    print(f"✅ Totaal {totaal_verwerkt} gezichten toegevoegd aan {DB_NAAM}.")

# --- Hoofdprogramma Uitvoeren ---
if __name__ == "__main__":
    
    if MAP_MET_FOTO_INDEX == "pad/naar/jouw/foto_collectie/om_te_indexeren":
        print("❌ FOUT: Pas het 'MAP_MET_FOTO_INDEX' pad aan in het script voordat je het uitvoert!")
    else:
        indexeer_map(MAP_MET_FOTO_INDEX)
