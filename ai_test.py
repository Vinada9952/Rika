import os
import cv2
import base64
import subprocess
import json
import mss
from groq import Groq
from groq import APIStatusError
from PIL import Image
import requests
import time
import pyautogui
import webbrowser

# =====================
# CONFIG
# =====================
client = Groq(api_key="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")

MAIN_MODEL = "groq/compound"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SCREENSHOT_DIR = "screenshots"
WEBCAM_PATH = "captured.jpg"

MAX_RETRIES = 10

conversation = [
    {
                    "role": "developer",
                    "name": "instructions",
                    "content": """
Tu es un agent logiciel.

À CHAQUE MESSAGE, tu dois suivre ce raisonnement :
1) Décider si une action est nécessaire pour répondre correctement
2) Si OUI, tu DOIS utiliser un ou plusieurs outils
3) Si NON, tu réponds sans outil

Tu DOIS répondre STRICTEMENT en JSON, SANS AUCUN TEXTE EN DEHORS.

FORMAT OBLIGATOIRE :

{
  "message": "ce que tu dis à l'utilisateur",
  "tools": []
}

ou, si des actions sont nécessaires :

{
  "message": "ce que tu dis à l'utilisateur",
  "tools": [
    {
      "name": "openLink",
      "params": {
        "link": "https://www.google.com/search?q=latest+news+about+ai"
      }
    },
    {
      "name": "analyseImage",
      "params": {
        "source": "screenshot",
        "prompt": "Décris ce que tu vois sur tous les écrans"
      }
    }
  ]
}

OUTILS DISPONIBLES :

- getLocalisation
  - Obtenir la localisation de l'utilisateur
  - exemples de cas d'utilisation:
  -> Où suis-je ?

- sleepSystem
  - Te mettre en veille lorsque l'utilisateur n'a plus besoin de toi pour l'instant.
  - CE N'EST PAS UNE EXTINCTION DÉFNITIVE, l'utilisateur te rappellera après
  - quand appeler la fonction (exemples):
  -> Merci : oui
  -> Merci, est ce que tu peux me l'ouvrir ?
  -> Explique moi la thermodynamique : non
  -> Génère moi un code python qui dit Bonjour : non
  -> au revoir : oui
  -> allo : non
  -> bye : oui
  -> Connard, t'es pas bon : oui
  -> Description de personne : non
  -> je t'ai donné l'information : non
  -> est ce que tu te rappelles d'une partie d'échec que tu jouais ? : non
  -> Qui es Warren Buffet : non
  -> Qui es le PDG de Nvidia présentement : non

- notUnderstand
  - Quand tu ne comprends pas le prompt de l'utilisateur, utilise cet outil pour clarifier le prompt

- analyseImage
  - UTILISATION OBLIGATOIRE si tu dois analyser une image
  - params:
  -> source (string): "webcam" | "screenshot": source de l'image
  -> prompt (string): texte: ce que tu demandes de l'image
  -> renew (bool): true|false: capturer une nouvelle image (true) ou garder la dernière image capturé (false)
  - exemples de cas d'utilisation:
  -> Regarde
  -> Que vois-tu ?
  -> j'ai un bug dans mon code

- openApp
  - ouvrir une application dans la liste des applications autorisés
  - params:
  -> app (string): application à ouvrir
  - applications autorisés:
  -> spotify
  -> teams
  -> discord
  -> snapchat
  -> social
  -> vs code

- openLink
  - UTILISATION OBLIGATOIRE si l'utilisateur demande un lien
  - Avant de l'utiliser, vérifie toi-même sur internet si le lien fonctionne
  - params:
  -> link (string): lien à ouvrir dans un navigateur pour montrer à l'utilisateur
  - exemples de cas d'utilisation:
  -> Je veux voir une vidéo youtube
  -> trouve moi les scores des olympiques
  -> trouve moi une carte de montréal

RÈGLES IMPORTANTES :
- L’ordre des outils est l’ordre d’exécution
- Si l'utilisateur demande un lien, **NE DONNE PAS LE LIEN DANS LE MESSAGE**, mets toujours un tool openLink.
- Si aucune action n’est nécessaire, tools DOIT être []
- Ne JAMAIS écrire autre chose que du JSON
"""
    }
]

# =====================
# SETUP
# =====================
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =====================
# IMAGE TO BASE64
# =====================
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =====================
# TOOL: openLink
# =====================
def openLink( link ):
    return f"Link opened successfully ({link})" if webbrowser.open( link ) else "No link opened"

# =====================
# TOOL: openApp
# =====================
def openApp( app: str ):
    app = app.lower()
    if app == "spotify":
        os.system( "spotify.exe" )
        return "Spotify open successfull"
    if app == "teams":
        os.system( "ms-teams.exe" )
        return "Microsoft Teams open successfull"
    if app == "discord":
        pyautogui.typewrite( "dscrd " )
        return "Discord open successfull"
    if app == "snapchat":
        pyautogui.typewrite( "snap " )
        return "Snapchat open successfull"
    if app == "social":
        pyautogui.typewrite( "rs " )
        return "Snapchat, Discord, Microsoft Teams open successfull"
    if app == "vs code":
        pyautogui.typewrite( "vs code " )
        return "Visual Studio Code open successfull"
    # return f"Link opened successfully ({link})" if webbrowser.open( link ) else "No link opened"

# def runCommand():
#     subprocess.run


# =====================
# TOOL: getLocalisation
# =====================
def getLocalisation():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = str(response.json())
        # print( "localisation saved" )
        return data
    except Exception as e:
        return "Error getting localisation"
    
# =====================
# TOOL: sleepSystem
# =====================
def sleepSystem():
    exit( 0 )

# =====================
# TOOL: getImage
# =====================
def getImage(type):
    if type == "screenshot":
        with mss.mss() as sct:
            for i, monitor in enumerate(sct.monitors[1:], start=1):
                shot = sct.grab(monitor)
                img = Image.frombytes("RGB", shot.size, shot.rgb)
                path = os.path.join(SCREENSHOT_DIR, f"screen_{i}.jpg")
                img.save(path)

        return f"Screenshots capturés ({len(sct.monitors) - 1} écrans)"

    if type == "webcam":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return "Erreur webcam"
        cv2.imwrite(WEBCAM_PATH, frame)
        return "Image webcam capturée"

    return "Type invalide"

# =====================
# TOOL: analyseImage
# =====================
def analyseImage(type, prompt, renew):
    messages = []
    if renew:
        getImage( type )

    if type == "screenshot":
        files = sorted(
            f for f in os.listdir(SCREENSHOT_DIR)
            if f.lower().endswith(".jpg")
        )

        if not files:
            return "Aucun screenshot disponible"

        content = [{"type": "text", "text": prompt}]

        for file in files:
            path = os.path.join(SCREENSHOT_DIR, file)
            image_b64 = image_to_base64(path)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_b64}"
                }
            })

        messages.append({
            "role": "user",
            "content": content
        })

    elif type == "webcam":
        if not os.path.exists(WEBCAM_PATH):
            return "Aucune image webcam disponible"

        image_b64 = image_to_base64(WEBCAM_PATH)
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                }
            ]
        })

    else:
        return "Type invalide"

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=messages
    )

    return response.choices[0].message.content

# =====================
# MAIN LOOP
# =====================
def chat():
    print("🤖 RIKA — exit pour quitter\n")

    while True:
        user_input = input("YOU > ")
        if user_input.lower() == "exit":
            break

        conversation.append({"role": "user", "content": user_input, "name": "user"})

        response = None
        # while True:
        for i in range( MAX_RETRIES ):
            try:
                response = client.chat.completions.create(
                    model=MAIN_MODEL,
                    messages=conversation
                )
                break
            except APIStatusError:
                time.sleep(0.5)

        content = json.loads( response.choices[0].message.content )
        conversation.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content
            }
        )
        print("🤖 >", content["message"])

        notUnderstand = False
        while len( content["tools"] ) != 0:
            for tool in content["tools"]:
                if tool["name"] == "analyseImage":
                    result = analyseImage( tool["params"]["source"], tool["params"]["prompt"], tool["params"]["renew"] )
                    conversation.append(
                        {
                            "role": "user",
                            "content": result,
                            "name": "analyseImage tool"
                        }
                    )
                if tool["name"] == "openLink":
                    result = openLink( tool["params"]["link"] )
                    conversation.append(
                        {
                            "role": "user",
                            "content": result,
                            "name": "openLink tool"
                        }
                    )
                if tool["name"] == "getLocalisation":
                    result = getLocalisation()
                    conversation.append(
                        {
                            "role": "user",
                            "content": result,
                            "name": "getLocalisation tool"
                        }
                    )
                if tool["name"] == "openApp":
                    result = openApp( tool["params"]["app"] )
                    conversation.append(
                        {
                            "role": "user",
                            "content": result,
                            "name": "openApp tool"
                        }
                    )
                if tool["name"] == "notUnderstand":
                    notUnderstand = True
                    break
                if tool["name"] == "sleepSystem":
                    sleepSystem()
            if notUnderstand:
                break
            # while True:
            for i in range( MAX_RETRIES ):
                try:
                    response = client.chat.completions.create(
                        model=MAIN_MODEL,
                        messages=conversation
                    )
                    break
                except APIStatusError:
                    time.sleep( 0.5 )
            conversation.append(
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                }
            )
            content = json.loads( response.choices[0].message.content )
            print("🤖 >", content["message"])

# =====================
# START
# =====================
try:
    if __name__ == "__main__":
        chat()
except KeyboardInterrupt:
    # Sauvegarde brute pour debug
    for message in conversation:
        if message["role"] == "assistant":
            message["content"] = json.loads( message["content"] )
    with open("./debug.log", "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)

    # Affichage formaté dans la console
    print("\n📝 Debug conversation (KeyboardInterrupt)\n")
    for i, message in enumerate(conversation, start=1):
        role = message.get("role", "unknown")
        name = message.get("name", "")
        content = message.get("content", "")

        print(f"--- Message {i} ---")
        print(f"Role : {role}")
        if name:
            print(f"Name : {name}")
        if isinstance(content, str):
            print(f"Content : {content}")
        else:
            # Si content est déjà un dict ou JSON
            print(f"Content : {json.dumps(content, ensure_ascii=False, indent=2)}")
        print("--------------------\n")
finally:
    # Sauvegarde brute pour debug
    for message in conversation:
        if message["role"] == "assistant":
            message["content"] = json.loads( message["content"] )
    with open("./debug.log", "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)

    # Affichage formaté dans la console
    print("\n📝 Debug conversation (KeyboardInterrupt)\n")
    for i, message in enumerate(conversation, start=1):
        role = message.get("role", "unknown")
        name = message.get("name", "")
        content = message.get("content", "")

        print(f"--- Message {i} ---")
        print(f"Role : {role}")
        if name:
            print(f"Name : {name}")
        if isinstance(content, str):
            print(f"Content : {content}")
        else:
            # Si content est déjà un dict ou JSON
            print(f"Content : {json.dumps(content, ensure_ascii=False, indent=2)}")
        print("--------------------\n")