import cv2
import pyautogui

cap = cv2.VideoCapture( 3 )


def captureImage( filename="captured_image.png", cam_mode="webcam" ):
    if cam_mode == "webcam":
        # print( 1 )
        # Ouvrir la caméra

        if not cap.isOpened():
            print("Erreur : Impossible d'ouvrir la caméra.")
            return

        # Lire une image de la caméra
        ret, frame = cap.read()

        if ret:
            # Enregistrer l'image dans un fichier
            cv2.imwrite(filename, frame)
            print(f"Image enregistrée sous {filename}.")
        else:
            print("Erreur : Impossible de capturer l'image.")

        # Libérer la caméra
        cap.release()
    elif cam_mode == "screenshot":
        pyautogui.screenshot( filename )

    # shutil.copyfile( f"./{filename}", f"./visual-memory/{moment().replace( ' ', '_' )}.png" )

captureImage()