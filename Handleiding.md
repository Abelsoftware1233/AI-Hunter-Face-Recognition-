# Gebruikershandleiding voor AI-Hunter-Face-Recognition

Dit project werkt in drie fasen: **1. Indexeren**, **2. Controleren** en **3. Zoeken**.

## Fase 1: Database Indexeren (Eénmalig)

Voordat je kunt zoeken, moet je de database vullen met je bekende foto's.

1.  **Plaats alle bekende foto's** die je wilt doorzoeken in één map (bijv. `/mijn_collectie/`). Zorg ervoor dat de bestandsnaam de naam van de persoon is (bijv. `Peter.jpg`, `Marie.png`).
2.  **Open `index_builder.py`** en pas de variabele `MAP_MET_FOTO_INDEX` aan naar het pad van je collectiemap.
    ```python
    MAP_MET_FOTO_INDEX = "C:/Gebruikers/Jouwnaam/mijn_collectie" 
    ```
3.  **Voer het script uit** om de index te bouwen:
    ```bash
    python index_builder.py
    ```
    Dit maakt het bestand `gezichts_index.db` aan met alle gezichtscoderingen.

## Fase 2: Controleren van een Onbekende Foto

Gebruik het hoofdscript om een onbekende foto te matchen met je zojuist geïndexeerde database.

1.  **Voer het hoofdscript uit** met het pad naar de onbekende foto als argument:
    ```bash
    python main_runner.py pad/naar/onbekende_persoon.jpg
    ```
2.  **Resultaat:**
    * Als een match wordt gevonden, krijg je de **naam**, de **gelijkenis-afstand** en de **bron URL** (of lokaal pad) terug.
    * Als er geen match wordt gevonden binnen de ingestelde drempel (0.6), wordt gevraagd of je extern wilt zoeken.

## Fase 3: Extern Zoeken (Zoekmachines)

Als de lokale database geen resultaat geeft, kun je de zoektocht uitbreiden naar het internet.

1.  Wanneer **`main_runner.py`** vraagt of je extern wilt zoeken (en je 'j' antwoordt), start de logica in **`zoek_via_google.py`**.
2.  De webbrowser wordt automatisch geopend op de Google Afbeeldingen zoekpagina.
3.  **Volg de instructies op het scherm:** Klik op het camera-icoon op de Google-pagina om de onbekende foto handmatig te uploaden en de reverse image search te starten.

---

Met deze bestanden is je **AI-Hunter-Face-Recognition** software compleet en klaar om te installeren en te gebruiken!
