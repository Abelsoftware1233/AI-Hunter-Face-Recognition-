import face_recognition
import cv2
import sys

# Dit is een CONCEPTUEEL script dat de basis van gezichtsherkenning demonstreert.
# Het is NIET ontworpen om het hele web te doorzoeken.

def detecteer_en_codeer_gezicht(afbeeldingspad):
    """
    Detecteert gezichten in een afbeelding, toont het aantal en maakt een codering (embedding) aan.
    
    Args:
        afbeeldingspad (str): Het pad naar de lokale afbeeldingsbestand.
    """
    
    print(f"Start analyse van: {afbeeldingspad}")
    
    try:
        # 1. Laad de afbeelding
        afbeelding = face_recognition.load_image_file(afbeeldingspad)

        # 2. Zoek alle gezichts locaties in de afbeelding
        gezichts_locaties = face_recognition.face_locations(afbeelding)
        aantal_gezichten = len(gezichts_locaties)
        
        print(f"\n✅ Resultaat: {aantal_gezichten} gezicht(en) gevonden.")
        
        if aantal_gezichten == 0:
            return None, None
            
        # 3. Maak gezichtscoderingen (embeddings) aan. Dit zijn de 'unieke nummers'.
        gezichts_coderingen = face_recognition.face_encodings(afbeelding, gezichts_locaties)
        
        print(f"✅ Coderingen (embeddings) gegenereerd voor {len(gezichts_coderingen)} gezicht(en).")
        print("   De eerste codering begint met:", gezichts_coderingen[0][:5], "...")
        
        # 4. Optioneel: Visuele demonstratie (vereist OpenCV)
        afbeelding_cv = cv2.imread(afbeeldingspad)
        for i, (top, right, bottom, left) in enumerate(gezichts_locaties):
            # Teken een rood rechthoek rond het gezicht
            cv2.rectangle(afbeelding_cv, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(afbeelding_cv, f"Gezicht {i+1}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        cv2.imshow("Gevonden Gezichten - Druk op een toets om te sluiten", afbeelding_cv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return gezichts_locaties, gezichts_coderingen

    except FileNotFoundError:
        print(f"\n❌ Fout: Bestand niet gevonden op het pad: {afbeeldingspad}")
        return None, None
    except Exception as e:
        print(f"\n❌ Er is een algemene fout opgetreden: {e}")
        print("Zorg ervoor dat de bibliotheken 'face_recognition' en 'opencv-python' correct zijn geïnstalleerd.")
        return None, None

# --- Voorbeeldgebruik ---
# VERVANG 'jouw_foto.jpg' door het ECHTE pad naar een foto op je computer.
# Zorg ervoor dat de foto in dezelfde map staat als dit script, of geef het volledige pad op.

if __name__ == "__main__":
    
    # Gebruikers moeten dit pad aanpassen
    if len(sys.argv) > 1:
        pad_naar_foto = sys.argv[1]
    else:
        # Dit is de standaard placeholder. Pas dit aan!
        pad_naar_foto = "pad/naar/jouw/persoonsfoto.jpg" 
        print(f"LET OP: Gebruik: python scriptnaam.py [pad_naar_foto]. Nu wordt de placeholder '{pad_naar_foto}' gebruikt.")

    locaties, coderingen = detecteer_en_codeer_gezicht(pad_naar_foto)

    # De codering is nu klaar om vergeleken te worden met andere coderingen in een database.
    
