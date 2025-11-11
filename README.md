# AI-Hunter-Face-Recognition-
# AI-Hunter-Face-Recognition - Gezichtsherkenningssoftware

Dit project bouwt een lokale gezichtsherkennings- en zoekmachine. Het combineert Computer Vision (met de `face-recognition` bibliotheek) met een lokale database (SQLite) om snel onbekende gezichten te matchen met een geïndexeerde collectie foto's.

## ⚠️ Disclaimer

Dit project is uitsluitend bedoeld voor educatieve doeleinden en het demonstreren van Computer Vision-technologie. Het ongeoorloofd verzamelen en verwerken van persoonlijke, biometrische gegevens is illegaal onder privacywetgeving (zoals de AVG/GDPR). Gebruik dit gereedschap altijd **verantwoordelijk** en met **uitdrukkelijke toestemming** van de gefotografeerde personen.

## 🚀 De Bouwstenen

| Bestand | Functie |
| :--- | :--- |
| `database_index.py` | Stelt de SQLite database op en zorgt voor opslag van de 128-dimensionale gezichtscoderingen. |
| `index_builder.py` | Leest een map met bekende foto's in, codeert ze en vult de database. |
| **`main_runner.py`** | Het centrale script. Codeert een onbekende foto en zoekt de beste match in de database. |
| `gezichts_vergelijker.py` | (Basis logica) Bevat de kerncode voor het berekenen van de afstand tussen twee gezichten. |
| `zoek_via_google.py` | Start een reverse image search in de browser als de lokale database geen match vindt. |
| `requirements.txt` | Lijst van alle benodigde Python bibliotheken. |

## 🛠️ Installatie

1.  Zorg ervoor dat Python 3.x is geïnstalleerd.
2.  Navigeer naar de projectmap in je terminal.
3.  Installeer alle benodigde pakketten:
    ```bash
    pip install -r requirements.txt
    ```
4.  Lees de volledige handleiding in de volgende sectie.
