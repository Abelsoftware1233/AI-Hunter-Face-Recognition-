import sqlite3
import numpy as np
import io

# Dit is een CONCEPTUEEL script dat de structuur van de database en de
# opslag van gezichtscoderingen demonstreert.

DB_NAAM = "gezichts_index.db"

# Functies om NumPy arrays (de coderingen) om te zetten naar en van de database
def adapt_array(arr):
    """Converteert een NumPy array naar een binaire string voor opslag in SQLite."""
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    """Converteert binaire string uit SQLite terug naar een NumPy array."""
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Registreer de converters zodat SQLite weet hoe met de coderingen om te gaan
sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("NUMPY_ARRAY", convert_array)

def maak_database_tabel(conn):
    """Maakt de tabel aan voor het opslaan van gezichtscoderingen en URL's."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Gezichten (
            id INTEGER PRIMARY KEY,
            naam TEXT NOT NULL,
            gezichts_codering NUMPY_ARRAY,
            bron_url TEXT
        )
    """)
    conn.commit()
    print(f"✅ Tabel 'Gezichten' is gecontroleerd/aangemaakt in {DB_NAAM}.")

def voeg_gezicht_toe(conn, naam, codering, url):
    """Voegt een nieuwe gezichtscodering en bijbehorende URL toe aan de index."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Gezichten (naam, gezichts_codering, bron_url) VALUES (?, ?, ?)", 
                   (naam, codering, url))
    conn.commit()
    print(f"✅ Gezicht van '{naam}' toegevoegd aan de index.")

def haal_alle_coderingen_op(conn):
    """Haalt alle coderingen en namen uit de database op."""
    cursor = conn.cursor()
    # Let op: de converter 'NUMPY_ARRAY' zorgt ervoor dat de data terugkomt als NumPy array.
    cursor.execute("SELECT naam, gezichts_codering, bron_url FROM Gezichten")
    return cursor.fetchall()

# --- Voorbeeldgebruik ---
if __name__ == "__main__":
    # Maak verbinding met de database. Als het bestand niet bestaat, wordt het aangemaakt.
    conn = sqlite3.connect(DB_NAAM, detect_types=sqlite3.PARSE_DECLTYPES)
    
    maak_database_tabel(conn)

    # 1. Simuleer twee willekeurige gezichtscoderingen (normaal gesproken komen deze van face_recognition)
    # Gezichtscoderingen zijn 128-dimensionale NumPy arrays.
    sim_codering_1 = np.random.rand(128).astype('float64')
    sim_codering_2 = np.random.rand(128).astype('float64') * 0.9 # Net iets anders
    
    # 2. Voeg de gesimuleerde data toe aan de database
    voeg_gezicht_toe(conn, "Peter", sim_codering_1, "https://example.com/peter_foto.jpg")
    voeg_gezicht_toe(conn, "Marie", sim_codering_2, "https://example.com/marie_profielfoto.png")

    # 3. Haal de data weer op om te bewijzen dat de arrays correct zijn opgeslagen
    opgeslagen_data = haal_alle_coderingen_op(conn)
    print("\n--- Opgeslagen Data Teruggehaald ---")
    
    for naam, codering, url in opgeslagen_data:
        print(f"Naam: {naam}")
        print(f"  Coderingstype: {type(codering)}")
        print(f"  Codering Vorm: {codering.shape}")
        print(f"  Bron URL: {url}")
        
    conn.close()
    print("\n✅ Databaseverbinding gesloten.")
  
