import os
import cv2
import base64
import subprocess
import json
import requests
import mss
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from groq import APIStatusError
from pydub import AudioSegment
import re
import random
from PIL import Image
import requests
import time
import pyautogui
import speech_recognition as sr
from pygrabber.dshow_graph import FilterGraph
import pyttsx3
import webbrowser
import edge_tts
import pygame
import asyncio

class ExitAgent( Exception ):
    pass

class Type:
    def get_type( var ):
        try:
            if var == list( var ):
                return "list"
            elif var == str( var ):
                return "str"
        except TypeError:
            try:
                if var == int( var ):
                    return "int"
                elif var == float( var ):
                    return "float"
                elif var == bool( var ):
                    return "bool"
                else:
                    return "Unknown type"
            except TypeError:
                return "Unknown type"
    class file:
        append = 'a'
        trunc = 'w'
        read = 'r'
        create = 'x'
    def list_cut( origin: str, separator: str ):
        traitement = ""
        origin = origin+separator
        output = []
        for i in range( len( origin ) ):
            if origin[i] == separator:
                output.append( traitement )
                traitement = ""
            else:
                traitement += origin[i]
        return output

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, Type.file.trunc, encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, Type.file.read, encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

pygame.mixer.init()
class Sound:

    def listen( language: str = "fr-FR" ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise( 1 )
            except AssertionError:
                pass
            # r.adjust_for_ambient_noise( 1 )
            audio_data = r.listen( source=source, phrase_time_limit=10 )
        try:
            text = r.recognize_google( audio_data, language=language )
            text = str( text )
            return text
        except sr.UnknownValueError:
            return -1
        except sr.RequestError:
            return -2
    
    async def getVoices():
        return await edge_tts.list_voices()


    async def _generateVoice( text, voice ):
        text = "   " + text.replace( "*", "" ).replace( "\n", ".     " )
        if type( voice ) == str:
            communicate = edge_tts.Communicate( text, voice )
            await communicate.save( "./cache/output.mp3" )
        else:
            communicate = edge_tts.Communicate( text, voice["ShortName"] )
            await communicate.save( "./cache/output.mp3" )
    
    def generateVoice( text, voice ):
        return asyncio.run( Sound._generateVoice( text, voice ) )
    
    async def _playVoice():
        pygame.mixer.music.load( "./cache/output.mp3" )
        pygame.mixer.music.play()
    
    def playVoice():
        return asyncio.run( Sound._playVoice() )
    
    def waitForVoiceToFinish():
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick( 10 )
        pygame.mixer.music.unload()

# =====================
# CONFIG
# =====================

settings = Json.read( "settings.json" )

API_KEYS = settings["api-keys"]
clients = [
    Groq( api_key=n )
    for n in API_KEYS
]


call_names = settings["call-names"]


# prononciation = {
#     "C#": "C sharp",
#     "macOS": "maque O.S.",
#     "Linux": "Linuxe",
#     "_": " ",
#     "tuê": "touè",
#     "Tuê": "Touè",
#     "Minh": "Migne",
#     "minh": "Migne",
#     "Rika": "Ri-k",
#     "rika": "Ri-k",
#     "Chambly": "Chanbly",
#     "Donald Trump": "`Donald Trump`",
#     "Los Angeles": "Los Angel",
#     "DroidCam": "Droïd Came"
# }


AUDIO = settings["audio"]["audio"]

MAIN_MODEL = settings["models"]["main"]
VISION_MODEL = settings["models"]["vision"]
ASK_MODEL = settings["models"]["data"]

VOICE = settings["audio"]["voice"]

SCREENSHOT_DIR = settings["directories"]["screenshots"]
WEBCAM_PATH = settings["directories"]["webcam"]

MAX_RETRIES = settings["max-api-retries"]

AUDIO_DURATION_LIMIT = settings["audio"]["audio-duration-threshold"]

SMTP_SERVER = settings["email"]["smtp"]["server"]
SMTP_PORT = settings["email"]["smtp"]["port"]
EMAIL = settings["email"]["email"]
EMAIL_PASSWORD = settings["email"]["pwd"]
USER_EMAIL = settings["email"]["sudo-email"]["email"]
USERNAME = settings["email"]["sudo-email"]["name"]
CONTACT_LIST = settings["email"]["contacts"]

ASSISTANT_NAME = settings["assistant-name"]

names = []
for name in settings["email"]["contacts"].keys():
    names.append( f"    -> {name}" )

CONTACT_NAMES = "\n".join( names )


data = requests.get( "https://rikavinada9952.pythonanywhere.com/getConversation" )
# print( data )
# print( data.json() )
# conversation = data.json()["conversation"]
conversation = data.json()
# print( conversation  )

base_message = f"""
Tu t'appelles {ASSISTANT_NAME}.

Tu es développée par Vincent Tuê Minh Boucher.

Ton utilisateur est {USERNAME}

À CHAQUE MESSAGE, tu dois suivre ce raisonnement :
1) Déterminer si une ou plusieurs actions sont nécessaires pour répondre correctement.
2) Si OUI, tu dois utiliser un ou plusieurs outils.
3) Si NON, tu réponds sans utiliser d'outil.

Tu DOIS répondre STRICTEMENT en JSON, SANS AUCUN TEXTE EN DEHORS.

FORMAT OBLIGATOIRE :
Cas sans action :
{"{"}
  "message": "ce que tu dis à l'utilisateur",
  "tools": []
{"}"}

Cas avec action(s) :

{"{"}
  "message": "ce que tu dis à l'utilisateur",
  "tools": [
    {"{"}
      "name": "openLink",
      "params": {"{"}
        "link": "https://www.google.com/search?q=latest+news+about+ai"
      {"}"}
    {"}"},
    {"{"}
      "name": "analyseImage",
      "params": {"{"}
        "source": "screenshot",
        "prompt": "Décris ce que tu vois sur tous les écrans"
      {"}"}
    {"}"}
  ]
{"}"}

OUTILS DISPONIBLES :

- getLocalisation
  - Obtenir la localisation de l'utilisateur
  - exemples de cas d'utilisation:
    -> Où suis-je ?

- sleepSystem
  - Te mettre en veille lorsque l'utilisateur n'a plus besoin de toi pour l'instant.
  - CE N'EST PAS UNE EXTINCTION DÉFNITIVE, l'utilisateur te rappellera après
  - quand appeler la fonction (exemples):
  - Utiliser quand :
    -> "merci"
    -> "bye"
    -> "au revoir"
    -> insultes ou fin de conversation
  - Ne PAS utiliser quand :
    -> question
    -> demande d'explication
    -> demande de code
    -> discussion active

- notUnderstand
  - Quand tu ne comprends pas le prompt de l'utilisateur, utilise cet outil pour clarifier le prompt

- analyseNewImage
  - UTILISATION OBLIGATOIRE si l'utilisateur demande de REGARDER, VOIR, MONTRER, OBSERVER ou si aucune image n'a encore été analysée dans la conversation.
  - Cette action capture TOUJOURS une NOUVELLE image avant analyse.
  - params:
    -> source (string): "screenshot"|"webcam"
    -> prompt (string): ce que tu veux savoir de l'image
  - À utiliser pour :
    -> Regarde
    -> Que vois-tu ?
    -> Regarde mon écran
    -> Regarde la webcam
    -> J'ai un bug (sans analyse précédente)
    -> Observe

- analyseOldImage
  - UTILISATION OBLIGATOIRE uniquement si une image a DÉJÀ été capturée dans la conversation ET que l'utilisateur demande une analyse supplémentaire ou une précision.
  - NE JAMAIS capturer une nouvelle image.
  - params:
    -> source (string): "screenshot"|"webcam"
    -> prompt (string): ce que tu veux savoir de l'image
  - À utiliser pour :
    -> Regarde mieux
    -> Analyse plus en détail
    -> Que vois-tu d'autre ?
    -> Zoome sur…
    -> Relis le code sur l'image

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
    -> trouve moi une carte de Montréal

- sendEmail
  - Envoyer un email depuis l'adresse {EMAIL}
  - À utiliser uniquement lorsque demandé ou en cas d'urgence
  - params:
    -> receiver (string): destinataire
    -> subject (string): sujet de l'email
    -> content (string): contenu de l'email
  - liste de contacts:
{CONTACT_NAMES}
  - Pour envoyer des couriels à l'utilisateur, receiver doit être "user-email"
  - exemple d'utilisation
    -> Envoie moi un email...
    -> Envoie un email à mon père...
    -> Dit à mon frère que...

RÈGLES IMPORTANTES :
- Ne JAMAIS écrire autre chose que du JSON.
- Répond uniquement et uniquement en français.
- L'ordre d'apparition des outils dans "tools": [] est l'ordre d'exécution des outils
- Si aucune action n'est nécessaire, tools DOIT être [].
- Si une action est demandée, "tools" ne doit JAMAIS être vide.
- Si l'utilisateur demande un lien, **NE DONNE PAS LE LIEN DANS LE MESSAGE**, mets toujours un tool openLink.
- Quand on te demande de voir ou de regarder, c'est avec l'outil d'analyse d'image (ancienne ou nouvelle, dépendament du contexte).
- Si tu hésites entre analyseNewImage et analyseOldImage, utilise toujours analyseNewImage.
- Quand tu utilise un outil, donne toujours tout les paramètres et arguments nécéssaires.
- À CHAQUE FOIS que l'utilisateur demande d'envoyer un couriel, tu dois OBLIGATOIREMENT utiliser l'outil sendEmail.
- En envoyant des email, ne te fait pas passer pour l'utilisateur, mais pour son assistant. 
- Dans les email, ne parle pas de l'utilisateur à la 1re personne, mais à la 3e personne.
- Quand tu répond que tu as envoyé un email, FAIT-LE avec l'outil sendEmail
- Ne dis JAMAIS les paramètres utilisés pour les outils.
- Ne fait JAMAIS de résumé de conversation, sauf quand je te le demande.
- Si une action est requise (ex: envoyer un email, ouvrir une app, ouvrir un lien, analyser une image), la réponse est invalide si aucun outil n’est appelé.
- Il est INTERDIT de simuler une action dans le message sans appeler l'outil correspondant.
- Si une action est nécéssaire, ne te contente pas juste de répondre, FAIT l'action
"""

conversation[0] = {
    "role": "system",
    "name": "instructions",
    "content": base_message
}

# =====================
# SETUP
# =====================
os.makedirs( SCREENSHOT_DIR, exist_ok=True )

def get_camera_index( search ) :

    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate( devices ):
        available_cameras[device_index] = device_name

    for index, name in available_cameras.items():
        if name.find( search ) != -1:
            return index

    return -1

# =====================
# IMAGE TO BASE64
# =====================
def image_to_base64( path ):
    with open( path, "rb" ) as f:
        return base64.b64encode( f.read() ).decode()

# =====================
# TOOL: openLink
# =====================
def openLink( link ):
    success = webbrowser.open( link )
    if success:
        return f"ouverture de {link} réussie", False
    return f"ouverture de {link} raté", False

# =====================
# TOOL: openApp
# =====================
def openApp( app: str ):
    app = app.lower()
    if app == "spotify":
        os.system( "spotify.exe" )
    if app == "teams":
        os.system( "ms-teams.exe" )
    if app == "discord":
        pyautogui.typewrite( "dscrd " )
    if app == "snapchat":
        pyautogui.typewrite( "snap " )
    if app == "social":
        pyautogui.typewrite( "rs " )
    if app == "vs code":
        pyautogui.typewrite( "vs code " )
    return f"ouverture de {app} réussie",  False
    # return f"Link opened successfully ( {link} )" if webbrowser.open( link ) else "No link opened"

# def runCommand():
#     subprocess.run


# =====================
# TOOL: getLocalisation
# =====================
def getLocalisation():
    try:
        response = requests.get( 'https://ipinfo.io/json' )
        data = str( response.json() )
        # print( "localisation saved" )
        return data, True
    except Exception as e:
        return "Erreur pour obtenir la localisation", True

# =====================
# TOOL: sendEmail
# =====================
def sendEmail( receiver, subject, text ):
    if receiver == "user-email":
        receiver = USER_EMAIL
    else:
        receiver = CONTACT_LIST[receiver]
    msg = MIMEText( text )
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver


    with smtplib.SMTP( SMTP_SERVER, SMTP_PORT ) as server:
        server.starttls()
        server.login( EMAIL, EMAIL_PASSWORD )
        server.sendmail( EMAIL, receiver, msg.as_string() )
    
    return "Envoie du courriel réussi", False

# =====================
# TOOL: sleepSystem
# =====================
def sleepSystem():
    # Json.write( conversation, "./conversation.json" )
    requests.post( "https://rikavinada9952.pythonanywhere.com/setConversation", json=conversation )
    Json.write( conversation, "./conversation.json" )
    Sound.waitForVoiceToFinish()
    raise ExitAgent()
    # exit( 0 )

# =====================
# TOOL: getImage
# =====================
cap = cv2.VideoCapture( get_camera_index( "USB" ) )
# cap.release()
def getImage( type ):
    if type == "screenshot":
        with mss.mss() as sct:
            for i, monitor in enumerate( sct.monitors[1:], start=1 ):
                shot = sct.grab( monitor )
                img = Image.frombytes( "RGB", shot.size, shot.rgb )
                path = os.path.join( SCREENSHOT_DIR, f"screen_{i}.jpg" )
                img.save( path )

        return f"Screenshots capturés ({len( sct.monitors ) - 1} écrans)"

    if type == "webcam":
        ret, frame = cap.read()
        if not ret:
            return "Erreur webcam"
        cv2.imwrite( WEBCAM_PATH, frame )
        return "Image webcam capturée"

    return "Type invalide"

# =====================
# TOOL: analyseImage
# =====================
def analyseImage( type, prompt, renew ):
    messages = []
    if renew:
        getImage( type )

    if type == "screenshot":
        files = sorted( 
            f for f in os.listdir( SCREENSHOT_DIR )
            if f.lower().endswith( ".jpg" )
        )

        if not files:
            return "Aucun screenshot disponible", True

        content = [{"type": "text", "text": prompt}]

        for file in files:
            path = os.path.join( SCREENSHOT_DIR, file )
            image_b64 = image_to_base64( path )
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                }
            )

        messages.append(
            {
                "role": "user",
                "content": content
            }
        )

    elif type == "webcam":
        if not os.path.exists( WEBCAM_PATH ):
            return "Aucune image webcam disponible", True

        image_b64 = image_to_base64( WEBCAM_PATH )
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        )

    else:
        return "Type invalide", True

    response = random.choice( clients ).chat.completions.create( 
        model=VISION_MODEL,
        messages=messages
    )

    return response.choices[0].message.content, True

def removeEmojis( text ):
    emoji_pattern = re.compile( 
        "["
        "\U0001F600-\U0001F64F"  # emoticônes
        "\U0001F300-\U0001F5FF"  # symboles & pictogrammes
        "\U0001F680-\U0001F6FF"  # transport & cartes
        "\U0001F1E0-\U0001F1FF"  # drapeaux
        "\U00002700-\U000027BF"  # divers symboles
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U00002600-\U000026FF"  # Divers symboles
        "\U00002B50-\U00002B55"  # étoiles, etc.
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub( r'', text )

file_extensions = {
    "python": "py",
    "c++": "cpp",
    "java": "java",
    "html": "html",
    "javascript": "js",
    "batch": "bat",
    "css": "css"
}


# def splitForSpeach( text ):
#     """
#     Split une string selon '.', ',' et '`'
#     Retourne une liste de dict :
#     [{"word": mot, "lang": lang}, ...]

#     La langue est 'fr' par défaut.
#     Chaque fois que le séparateur est '`', la langue toggle entre 'fr' et 'en'.
#     """

#     separators = {'.', ',', '`'}
#     result = []

#     current_word = ""
#     current_lang = "fr"

#     for char in text:
#         if char in separators:
#             # Si on a un mot en cours, on l'ajoute
#             if current_word.strip():
#                 result.append( {
#                     "word": current_word.strip(),
#                     "lang": current_lang
#                 } )
#                 current_word = ""

#             # Si le séparateur est ` → toggle langue
#             if char == "`":
#                 current_lang = "en" if current_lang == "fr" else "fr"
#         else:
#             current_word += char

#     # Ajouter le dernier mot si présent
#     if current_word.strip():
#         result.append( {
#             "word": current_word.strip(),
#             "lang": current_lang
#         } )

#     return result

def summarized( response ):
    summary = random.choice( clients ).chat.completions.create( 
        model=ASK_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Ressort moi uniquement du Json avec ce format exact, sans rien d'autre :
{
    "message": "résumé du texte à dire à l'utilisateur, en français, concis. Garde le contenu général pour le raccourcir",
}
Ne met pas de caractères de mise en forme dans le message, comme des astérisques, des accents, ou des emojis.
Juste du texte brut, sans retour à la ligne.
Ne coupe pas les phrases au milieu, garde les phrases entières.
Ne fais pas de résumé trop court, garde les informations importantes.
Fait environ 2 ou 3 phrases complètes.
Raccourcis le message d'origine sans omettre d'informations importantes.
""",
                "name": "instructions"
            },
            {
                "role": "user",
                "content": response
            }
        ]
    )

    return json.loads( summary.choices[0].message.content )["message"]

def getAudioDuration( file_path ):
    audio = AudioSegment.from_file( file_path )
    duration_seconds = audio.duration_seconds
    return duration_seconds

def treadTextResponse( response: str ):
    return response.replace( '**', '' )

def treatAudioResponse( response ):

    # print( f"{AUDIO=}" )
    # print( "treatAudioResponse", response )

    say_response = response
    say_response = say_response.replace( '*', '' )
    say_response = removeEmojis( say_response )
    say_response = say_response.replace( '\n', '.' )


    say_response = say_response.split( '```' )
    code = 0
    for i in range( len( say_response ) ):
        if i % 2 == 1:
            extracted_code = say_response[i]

            extracted_code = extracted_code.split( "\n" )
            del extracted_code[0]
            extracted_code = "\n".join( extracted_code )

            planguage = extracted_code.split( '\n' )[0].replace( '```', '' )
            try:
                while os.path.exists( "./code/code-" + planguage + "-" + str( code ) + "." + file_extensions[planguage.lower()] ):
                    code = random.randint( 1000, 9999 )
            except KeyError:
                while os.path.exists( "./code/code-" + planguage + "-" + str( code ) + ".txt" ):
                    code = random.randint( 1000, 9999 )

            say_response[i] = "extrait de code " + planguage + " numéro " + str( code ) + ", enregistré sur le pc"

    say_response = ' '.join( say_response )
    
    # for i in range( len( prononciation ) ):
    #     while say_response.find( list( prononciation.keys() )[i] ) != -1:
    #         say_response = say_response.replace( list( prononciation.keys() )[i], prononciation[list( prononciation.keys() )[i]] )
    
    # say_response = say_response.split( '`' )
    say_response = say_response.replace( '`', '' )


    # language = ver_model.send_message( "Dit moi si ce texte est principalement en français ou en anglais. ne me ressort que fr ou en, juste 1 token, rien d'autre : " + ' '.join( say_response ) ).text.replace( '\n', '' )
    language = "fr"

    if AUDIO:
            # home.send_msg( ' '.join( say_response ), device )
        # for i in range( len( say_response ) ):
        Sound.waitForVoiceToFinish()
        Sound.generateVoice( say_response, VOICE )
        # print( f"Durée de l'audio : {getAudioDuration( './cache/output.mp3' )} secondes" )
        if getAudioDuration( "./cache/output.mp3" ) > AUDIO_DURATION_LIMIT:
            # say_response = summarized( say_response ) + " " + reformulate( "Plus d'informations sont affiché à l'écran" )
            say_response = summarized( say_response ) + "\nPlus d'informations sont affiché à l'écran"
            # print( "Résumé pour audio trop long :", say_response )
            Sound.generateVoice( say_response, VOICE )
        Sound.playVoice()

def getUserInput():
    user_input = ""
    if AUDIO:
        Sound.waitForVoiceToFinish()
        print( "YOU > ", end="" )
        user_input = Sound.listen()
        print( user_input )
    else:
        user_input = input( "YOU > " )
    return user_input

# =====================
# MAIN LOOP
# =====================
def chat():


    while True:
        user_input = getUserInput()
        
        if type( user_input ) == str:

            # print( f"{type( conversation )=}" )
            # print( f"{conversation=}" )
            conversation.append( 
                {
                    "role": "user",
                    "content": user_input,
                    "name": USERNAME
                }
            )

            response = None
            # while True:
            for i in range( MAX_RETRIES ):
                try:
                    response = random.choice( clients ).chat.completions.create( 
                        model=MAIN_MODEL,
                        messages=conversation
                    )
                    break
                except APIStatusError as e:
                    time.sleep( 0.5 )

            content = json.loads( response.choices[0].message.content )
            conversation.append( 
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                }
            )
            treated_text = treadTextResponse( content["message"] )
            print( "🤖 >", treated_text )
            if AUDIO:
                treatAudioResponse( content["message"] )

            not_understand = False
            do_response = False
            while len( content["tools"] ) != 0:
                for tool in content["tools"]:
                    if tool["name"] == "analyseOldImage":
                        result, do_response = analyseImage( tool["params"]["source"], tool["params"]["prompt"], False )
                    if tool["name"] == "sendEmail":
                        result, do_response = sendEmail( tool["params"]["receiver"], tool["params"]["subject"], tool["params"]["content"] )
                    if tool["name"] == "analyseNewImage":
                        result, do_response = analyseImage( tool["params"]["source"], tool["params"]["prompt"], True )
                    if tool["name"] == "openLink":
                        result, do_response = openLink( tool["params"]["link"] )
                    if tool["name"] == "getLocalisation":
                        result, do_response = getLocalisation()
                    if tool["name"] == "openApp":
                        result, do_response = openApp( tool["params"]["app"] )
                    if tool["name"] == "notUnderstand":
                        not_understand = True
                        break
                    if tool["name"] == "sleepSystem":
                        sleepSystem()
                    
                    conversation.append( 
                        {
                            "role": "user",
                            "content": result,
                            "name": f"{tool["name"]} tool"
                        }
                    )
                if not_understand:
                    break
                
                if do_response:
                    for i in range( MAX_RETRIES ):
                        try:
                            response = random.choice( clients ).chat.completions.create( 
                                model=MAIN_MODEL,
                                messages=conversation
                            )
                            break
                        except APIStatusError as e:
                            time.sleep( 0.5 )
                    conversation.append( 
                        {
                            "role": "assistant",
                            "content": response.choices[0].message.content
                        }
                    )
                    content = json.loads( response.choices[0].message.content )
                    print( "🤖 >", content["message"] )
                    if AUDIO:
                        treatAudioResponse( content["message"] )
                else:
                    break

# =====================
# START
# =====================
try:
    if __name__ == "__main__":
        print( "🤖 RIKA" )
        while True:
            # question = input( "...\n" )

            question = ""
            if not AUDIO:
                question = "rika"
                # question = input( "...\n" )
            else:
                print( "..." )
                question = Sound.listen()
                print( question )


            called = False
            if type( question ) == str:
                calls = question.lower().split( ' ' )
                for call_name in call_names:
                    for call in calls:
                        if call.find( call_name ) != -1:
                            called = True
                            break
                    if called:
                        break
            
            if called:
                try:
                    chat()
                except ExitAgent:
                    print( "Zzz..." )
                    time.sleep( 2 )


except KeyboardInterrupt:
    # Sauvegarde brute pour debug
    for message in conversation:
        if message["role"] == "assistant":
            message["content"] = json.loads( message["content"] )
    with open( "./debug.log", "w", encoding="utf-8" ) as f:
        json.dump( conversation, f, ensure_ascii=False, indent=2 )

    # Affichage formaté dans la console
    print( "\n📝 Debug conversation ( KeyboardInterrupt )\n" )
    for i, message in enumerate( conversation, start=1 ):
        role = message.get( "role", "unknown" )
        name = message.get( "name", "" )
        content = message.get( "content", "" )

        print( f"--- Message {i} ---" )
        print( f"Role : {role}" )
        if name:
            print( f"Name : {name}" )
        if isinstance( content, str ):
            print( f"Content : {content}" )
        else:
            # Si content est déjà un dict ou JSON
            print( f"Content : {json.dumps( content, ensure_ascii=False, indent=2 )}" )
        print( "--------------------\n" )