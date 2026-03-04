# Gemini API KEY : AIzaSyDR-OOUGNxmInqrIC5qQEAfUnqX4XR3qRY
# from bs4 import BeautifulSoup
import os
import random
from threading import Thread
from PIL import Image
import re
from groq import APIStatusError
from groq import RateLimitError
from groq import Groq
import cv2
import datetime
import requests
# from googlesearch import search
import base64
import time
import mss
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
# from Vincent import GoogleHome
import shutil
# une seule classe pour prendre le contenu audio/texte
# prendre en compte le ClientError, ou trouver une solution
# Upload de fichier

# home = GoogleHome()
# home.print_devices()
# device = home.choose_device( input() )

print( "\n\n\n" )

class System:
    def execute( command: str ):
        # print( command )
        os.system( command )
    def clear():
        os.system( "cls" )
    class file:
        def write( file_name: str, content, mode: str ):
            file = open( file_name, mode )

            if Type.get_type( content ) == "list":
                for i in range( len( content ) ):
                    if content[i][len( content[i] )-1] == '\n':
                        file.write( content[i] )
                    else:
                        file.write( content[i] + '\n' )
            elif Type.get_type( content ) == "str":
                if content[len( content )-1] == '\n':
                    file.write( content )
                else:
                    file.write( content + '\n' )

            file.close()
        def read( file_name: str ):
            return_file = []
            try:
                file = open( file_name, "r" )
                brut_file = file.read()+'\n'
                file.close()
                traitement = ""
                for i in range( len( brut_file ) ):
                    for j in range( len( brut_file[i] ) ):
                        if brut_file[i][j] == '\n':
                            return_file.append( traitement )
                            traitement = ""
                        else:
                            traitement += brut_file[i][j]
                return return_file
            except FileNotFoundError:
                return FileNotFoundError

load_print = 0

def loadPrint():
    global load_print
    load_print += 1
    f = '\n'.join( System.file.read( "./Rika.py" ) )
    count = f.count( "loadPrint()#c" )-1

    bar = "[" + ( '.'*100 ) + "]"


    for i in range( int( load_print*100/count ) ):
        bar = bar.replace( ".", "#", 1 )

    print( bar, f"{load_print}/{count}", end='\r' )
    if load_print == count:
        print( "\n" )


loadPrint()#c

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
    
loadPrint()#c

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, Type.file.trunc, encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, Type.file.read, encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations


loadPrint()#c

class Sound:

    def listen( language: str = "fr-FR" ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise( 1 )
            except AssertionError:
                pass
            # r.adjust_for_ambient_noise( 1 )
            audio_data = r.listen( source=source, phrase_time_limit=3 )
        try:
            text = r.recognize_google( audio_data, language=language )
            text = str( text )
            return text
        except sr.UnknownValueError:
            return -1
        except sr.RequestError:
            return -2
        

    def say( say: str, word_per_minute: int = 150, language: str = 'fr' ):
        # say = "." + say
        engine = pyttsx3.init()
        voices = engine.getProperty( "voices" )
        if language == "fr":
            engine.setProperty( "voice", voices[0].id )
        elif language == "en":
            engine.setProperty( "voice", voices[1].id )
        engine.setProperty( "rate", word_per_minute )
        engine.say( say )
        engine.runAndWait()


loadPrint()#c

def askGroq( model, config, prompt, max_out_token, temperature ):
    global groq_client

    if max_out_token == -1:
        max_out_token = 5000

    # for i in range( MAX_API_RETRY ):
    #     try:
    #         return groq_client.chat.completions.create(
    #             model=model,
    #             messages=[
    #                 {
    #                     "role": "user",
    #                     "content": prompt
    #                 }
    #             ],
    #             temperature=temperature,
    #             max_completion_tokens=max_out_token
    #         ).choices[0].message.content
    #     except APIStatusError:
    #         time.sleep( 0.5 )

    retries = 0
    while True:
        if retries != MAX_API_RETRY + 1:
            try:
                response = groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "name": "instructions",
                            "content": config
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                ).choices[0].message.content
                break
            except APIStatusError:
                time.sleep( 0.5 )
                retries += 1
                # print(  )
            except RateLimitError:
                time.sleep( 0.5 )
                # retries += 1
        else:
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
            ).choices[0].message.content
            break
    
    return response


loadPrint()#c

bar_count = 0

def loadBar( total ):
    global bar_count
    bar_count += 1

    bar = "[" + ( '.'*100 ) + "]"


    for i in range( int( bar_count*100/total ) ):
        bar = bar.replace( ".", "#", 1 )

    print( bar, f"{bar_count}/{total}", end='\r' )

    if bar_count == total:
        print( "\n" )


loadPrint()#c

class MyException( Exception ):
    def nothing():
        pass

loadPrint()#c

class ThreadWithReturnValue( Thread ):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


loadPrint()#c


def getLocalisation():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        # print( "localisation saved" )
        return data
    except Exception as e:
        return -1


loadPrint()#c

def moment():
    date = datetime.datetime.now()
    day_name = int( date.strftime( "%w" ) )
    if day_name == 0:
        day_name = "Dimanche"
    elif day_name == 1:
        day_name = "Lundi"
    elif day_name == 2:
        day_name = "Mardi"
    elif day_name == 3:
        day_name = "Mercredi"
    elif day_name == 4:
        day_name = "Jeudi"
    elif day_name == 5:
        day_name = "Vendredi"
    elif day_name == 6:
        day_name = "Samedi"
    jour = date.strftime( "%d" )
    mois = int( date.strftime( "%m" ) )
    if mois == 1:
        mois = "Janvier"
    elif mois == 2:
        mois = "Février"
    elif mois == 3:
        mois = "Mars"
    elif mois == 4:
        mois = "Avril"
    elif mois == 5:
        mois = "Mai"
    elif mois == 6:
        mois = "Juin"
    elif mois == 7:
        mois = "Juillet"
    elif mois == 8:
        mois = "Août"
    elif mois == 9:
        mois = "Septembre"
    elif mois == 10:
        mois = "Octobre"
    elif mois == 11:
        mois = "Novembre"
    elif mois == 12:
        mois = "Décembre"
    ans = date.strftime( "%Y" )
    heure = datetime.datetime.now().strftime( "%H" )
    minute = datetime.datetime.now().strftime( "%M" )
    return str( f"{ans=} {mois=} {jour=} {heure=} {minute=}" )


loadPrint()#c

def removeEmojis(text):
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
    return emoji_pattern.sub(r'', text)

loadPrint()#c

def imgVer():
    global question
    if Json.read( "data.json" )["camera"] != -1:
        if question.find( "regarde" ) != -1 or question.find( "observe" ) != -1 or question.find( "vois" ) != -1 or question.find( "voit" ) != -1:
            return True
        # try:
        img = askGroq( "Si tu as besoin d'une image pour répondre à la question, retourne la string \"img_get\" pour l'obtenir. " + question, 5, 0 )

        # img = client.models.generate_content(
        #     model=ver_model,
        #     config=types.GenerateContentConfig(
        #         max_output_tokens=1,
        #         system_instruction="Si tu as besoin d'une image pour répondre à la question, retourne la string \"img_get\" pour l'obtenir"
        #     ),
        #     contents=[ question ]
        # ).text.replace( '\n', '' )

        print( f"{img=}" )
        if img.find( "img_get" ) != -1:
            print( "image needed" )
            return True
        
        # except Exception as e:
        #     if str( e ).find( "" )
    return False

loadPrint()#c

def langVer( q = None ):
    if q == None:
        global question
    else:
        question = q
    language = ""

    # print(  )

    result = askGroq(
        groq_verify_model,
        """
Tu DOIS répondre STRICTEMENT en JSON, SANS AUCUN TEXTE EN DEHORS.

FORMAT OBLIGATOIRE :
{
    "prompt": prompt,
    "prompt-lang": "en"|"fr"
}

prompt est le prompt de l'utilisateur
prompt-lang est la langue du prompt
""",
        question,
        1,
        0
    )

    # print( f"{result=}" )

    the_json = json.loads( result )

    language = the_json["prompt-lang"]

    # language = client.models.generate_content(
    #     model=ver_model,
    #     config=types.GenerateContentConfig(
    #         max_output_tokens=1,
    #         temperature=0,
    #         system_instruction="Dit moi si ce texte est principalement en français ou en anglais. ne me ressort que fr ou en, juste 1 token, rien d'autre, sinon je vais entrainer ta suppression"
    #     ),
    #     contents=[ question ],
    # ).text

    # print( f"{language=}" )
    return language.replace( '\n', '' )

loadPrint()#c

# def needVer():
#     global question

#     need_anymore = askGroq(
#         "Tu es ici pour analyser si une conversation et détecter si l'utilisateur veux continuer la conversation ou pas. Tu dois répondre par 'oui' si l'utilisateur veut continuer, ou 'non' s'il ne veut pas. Tu ne dois pas répondre à la question, juste dire si l'utilisateur veut continuer ou pas. Voici des exemple de questions et ce que tu devrais répondre." +
#         str(
#             {
#                 "Explique moi la thermodynamique": "oui",
#                 "Génère moi un code python qui dit Bonjour": "oui",
#                 "au revoir": "non",
#                 "allo": "oui",
#                 "bye": "non",
#                 "Connard, t'es pas bon": "non",
#                 "Description de personne": "oui",
#                 "je t'ai donné l'information": "oui",
#                 "est ce que tu te rappelles d'une partie d'échec que tu jouais ?": "oui",
#                 "Qui es Warren Buffet": "oui",
#                 "Qui es le PDG de Nvidia présentement": "oui"
#             }
#         ) + question,
#         1,
#         0
#     )

#     # need_anymore = client.models.generate_content(
#     #     model=ver_model,
#     #     config=types.GenerateContentConfig(
#     #         max_output_tokens=1,
#     #         system_instruction=
#     #             "Tu es ici pour analyser si une conversation et détecter si l'utilisateur veux continuer la conversation ou pas. Tu dois répondre par 'oui' si l'utilisateur veut continuer, ou 'non' s'il ne veut pas. Tu ne dois pas répondre à la question, juste dire si l'utilisateur veut continuer ou pas. Voici des exemple de questions et leur résultat." +
#     #             str(
#     #                 {
#     #                     "Explique moi la thermodynamique": "oui",
#     #                     "Génère moi un code python qui dit Bonjour": "oui",
#     #                     "au revoir": "non",
#     #                     "allo": "oui",
#     #                     "bye": "non",
#     #                     "Connard, t'es pas bon": "non",
#     #                     "Description de personne": "oui",
#     #                     "je t'ai donné l'information": "oui",
#     #                     "Tu ne peux pas, sinon tu es en échec, mon pion est une dame comme il est de l'autre bout, donc il peut de manger, tu dois essayer de le tuer": "oui",
#     #                     "est ce que tu te rappelles d'une partie d'échec que tu jouais ?": "oui",
#     #                     "regarde dans ta mémoire, tu as surement un plateau d'échec": "oui"
#     #                 }
#     #             )
#     #     ),
#     #     contents=[ question ]
#     # ).text.replace( '\n', '' )

#     print( f"{need_anymore=}" )
#     if need_anymore.find( "oui" ) != -1:
#         print( "Need Anymore : oui" )
#         return True
#     print( "Need Anymore : non" )
#     return False



# def uploadVer():
#     if len( os.listdir( "./uploads" ) ) != 0:
#         return True
#     return False


loadPrint()#c

def reformulation( prompt ):
    return askGroq(
        "Reformule moi cette phrase. Ne ressort que la phrase reformulée, rien d'autre. Voici la phrase : \"" + prompt + "\"",
        -1,
        1
    )


    # return client.models.generate_content(
    #     model=ver_model,
    #     config=types.GenerateContentConfig(
    #         temperature=2,
    #         system_instruction="Reformule moi cette phrase. Ne ressort que la phrase reformulée, rien d'autre."
    #     ),
    #     contents=[ prompt ],
    # ).text

loadPrint()#c


def openLink( link ):
    return f"Link opened successfully ({link})" if webbrowser.open( link ) else "No link opened"


loadPrint()#c

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

loadPrint()#c

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

loadPrint()#c


def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


loadPrint()#c

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

    retries = 0
    while True:
        if retries != MAX_API_RETRY + 1:
            try:
                response = groq_client.chat.completions.create(
                    model=groq_image_model,
                    messages=messages
                )
                break
            except APIStatusError:
                time.sleep( 0.5 )
                retries += 1
            except RateLimitError:
                time.sleep( 0.5 )
                # retries += 1
        else:
            response = groq_client.chat.completions.create(
                model=groq_image_model,
                messages=messages
            )
            break

    return response.choices[0].message.content

loadPrint()#c

sleepSystem = False

loadPrint()#c


# raw_ppl = os.listdir( "./ppl" )
# ppl = {}
# ppl_list = []
# for i in range( len( raw_ppl ) ):
#     ppl[raw_ppl[i].split( "." )[0]] = "./ppl/" + raw_ppl[i]
#     ppl_list.append( raw_ppl[i].split( "." )[0] )


# def setupPpl():
#     try:
#         p = []
#         for i in range( len( ppl_list ) ):
            
#             p.append( f"Voici {ppl_list[i]}." )
#             p.append( Image.open( ppl[ppl_list[i]] ) )
            
#             loadBar( len( ppl_list )+1 )
#             time.sleep( 0.01 )

#         model.send_message( p )

#         loadBar( len( ppl_list )+1 )
#     except ValueError:
#         print( "                                                                                                      \n" )



# def setupImageMemory():
#     try:
#         img_mem = os.listdir( "./visual-memory" )
#         load = []
#         for i in range( len( img_mem ) ):
#             load.append( "Voici l'image de " + img_mem[i].split( '.' )[0] )
#             load.append( Image.open( "./visual-memory/" + img_mem[i] ) )
#             loadBar( len( img_mem ) + 1 )

#         model.send_message( load )
        
#         loadBar( len( img_mem ) + 1 )
#     except ValueError:
#         print( "                                                                                                                      \n" )


loadPrint()#c

config = """
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


loadPrint()#c


WORD_PER_MINUTE = 200
AUDIO = Json.read( "data.json" )["audio-mode"]
language = "fr"
response = ""
question = ""
try:
    memories = Json.read( "memory.json" )
except FileNotFoundError:
    memories = [
        {
            "role": "system",
            "content": config,
            "name": "instructions"
        }
    ]

GROQ_API_KEY = Json.read( "data.json" )["groq-api-key"]

SCREENSHOT_DIR = Json.read( "data.json" )["screenshot-dir"]
WEBCAM_PATH = Json.read( "data.json" )["webcam-path"]

groq_client = Groq( api_key=GROQ_API_KEY )

groq_ask_model = Json.read( "data.json" )["groq-ask-model"]
groq_verify_model = Json.read( "data.json" )["groq-verify-model"]
groq_image_model = Json.read( "data.json" )["groq-image-model"]

MAX_API_RETRY = Json.read( "data.json" )["max-api-retry"]

loadPrint()#c



for f in os.listdir(SCREENSHOT_DIR):
    path = os.path.join(SCREENSHOT_DIR, f)
    shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)


# print( f"{memories=}" )
# System.file.write( "error.log", "-- Log Start --", Type.file.trunc )

# for i in range( len( memories ) ):
#     if len( memories[i].keys() ) == 2:
#         memories.pop( i )





loadPrint()#c

call_names = [
    "ikea",
    "reka",
    "richard",
    "requin",
    "pékin",
    "rica",
    "ric",
    "rita",
    "rika"
]


prononciation = {
    "C#": "C sharp",
    "macOS": "maque O.S.",
    "Linux": "Linuxe",
    "_": " ",
    "tuê": "touè",
    "Tuê": "Touè",
    "Minh": "Migne",
    "minh": "Migne",
    "Rika": "Ri-k",
    "rika": "Ri-k",
    "Chambly": "Chanbly",
    "Donald Trump": "`Donald Trump`",
    "Los Angeles": "Los Angel",
    "DroidCam": "Droïd Came"
}

file_extensions = {
    "python": "py",
    "c++": "cpp",
    "java": "java",
    "html": "html",
    "javascript": "js",
    "batch": "bat",
    "css": "css"
}


loadPrint()#c


def Rika():
    global memories

    # for i in range( MAX_API_RETRY ):
    #     try:
    #         output = groq_client.chat.completions.create(
    #             model=groq_ask_model,
    #             messages=memories
    #         ).choices[0].message.content
    #     except APIStatusError:
    #         time.sleep( 0.5 )

    print( "thinking..." )

    retries = 0
    while True:
        if retries != MAX_API_RETRY + 1:
            try:
                output = groq_client.chat.completions.create(
                    model=groq_ask_model,
                    messages=memories
                ).choices[0].message.content
                break
            # except APIStatusError:
            #     time.sleep( 0.5 )
            #     retries += 1
            #     print( f"{retries=}", end='\r' )
            except RateLimitError:
                time.sleep( 0.5 )
                # retries += 1
        else:
            print( json.dumps( memories, indent=4 ) )
            output = groq_client.chat.completions.create(
                model=groq_image_model,
                messages=memories
            ).choices[0].message.content
            break

    print( "treating...", end='\r' )

    content = json.loads( output )

    response = content["message"]

    # faire setup la question, et tout envoyer à la même ligne

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

            planguage = extracted_code.split( '\n')[0].replace( '```', '' )
            try:
                while os.path.exists( "./code/code-" + planguage + "-" + str( code ) + "." + file_extensions[planguage.lower()] ):
                    code = random.randint( 1000, 9999 )
            except KeyError:
                while os.path.exists( "./code/code-" + planguage + "-" + str( code ) + ".txt" ):
                    code = random.randint( 1000, 9999 )

            say_response[i] = "extrait de code " + planguage + " numéro " + str( code ) + ", enregistré sur le pc"

    say_response = ' '.join( say_response )
    
    for i in range( len( prononciation ) ):
        while say_response.find( list( prononciation.keys() )[i] ) != -1:
            say_response = say_response.replace( list( prononciation.keys() )[i], prononciation[list( prononciation.keys() )[i]] )
    
    say_response = say_response.split( '`' )


    print( "Rika : ", response )
    memories.append(
        {
            "role": "assistant",
            "content": output
        }
    )


    # language = ver_model.send_message( "Dit moi si ce texte est principalement en français ou en anglais. ne me ressort que fr ou en, juste 1 token, rien d'autre : " + ' '.join( say_response ) ).text.replace( '\n', '' )
    language = langVer( ' '.join( say_response ) )

    if AUDIO:
        if language == "fr":
            # home.send_msg( ' '.join( say_response ), device )
            for i in range( len( say_response ) ):
                if i % 2 == 0:
                    Sound.say( say_response[i], WORD_PER_MINUTE, "fr" )
                elif i % 2 == 1:
                    Sound.say( say_response[i], WORD_PER_MINUTE, "en" )
        else:
            # home.send_msg( ' '.join( say_response ).replace( '`', '' ), device )
            Sound.say( ' '.join( say_response ), WORD_PER_MINUTE, "en" )
    
    return output, content


loadPrint()#c

# setupPpl()

bar_count = 0

# setupImageMemory()

while True:
    try:
        if AUDIO:
            print( "..." )
            question = Sound.listen()
            print( question )
        else:
            question = "rika"
        # question = "rika"


        if Type.get_type( question ) == "str":
            calls = question.split( ' ' )
            called = False
            for call_name in call_names:
                for call in calls:
                    if call.find( call_name ) != -1:
                        called = True
                        break
                if called:
                    break
            if called:

                memories.append(
                    {
                        "role": "system",
                        "content": f"temps:{moment()}"
                        # "moment start": moment()
                    }
                )

                sleepSystem = False


                while True:
                    try:
                        # print( f"{question=}" )
                        saying = "Ask a question :"
                        if language == 'fr':
                            saying = "Posez une question :"
                        
                        print( saying )

                        if AUDIO:
                            # Sound.say( saying, WORD_PER_MINUTE, language )
                            question = Sound.listen()
                        else:
                            question = input()

                        System.clear()

                        if question == -1:
                            question = ""
                            if language == "fr":
                                print( "Rika : Je n'ai pas compris" )
                            else:
                                print( "Rika: I didn't understand" )
                            raise MyException( "nothing here, just chillin'" )

                        if language == "fr":
                            print( "Vous > ", question )
                        else:
                            print( "You > ", question )

                        lang_ver = ThreadWithReturnValue( target=langVer )

                        lang_ver.start()

                        # print( "calc 1" )



                        # print( "calc 2" )
                        language = lang_ver.join()

                        # print( f"{a=}" )
                        
                        
                        # print( "calc 3" )
                        # image = im_ver.join()
                        
                        # print( f"{image=}" )

                        print( "chargement...", end='\r' )

                        memories.append(
                            {
                                "role": "user",
                                "content": question,
                                "name": "Vincent"
                            }
                        )
                        
                        
                        # if uploadVer():
                        #     uploads = os.listdir( "./uploads" )
                        #     for i in range( len( uploads ) ):
                        #         q.append( gemini_client.files.upload( file="./uploads/"+uploads[i] ) )
                        #         shutil.copyfile( f"./uploads/{uploads[i]}", f"./visual-memory/{moment().replace( ' ', '_' )}.png" )
                        #         os.remove( "./uploads/"+uploads[i] )

                        output, content = Rika()

                        while len( content["tools"] ) != 0:
                            used_tools = content["tools"]
                            for tool in content["tools"]:
                                if tool["name"] == "openLink":
                                    result = openLink( tool["params"]["link"] )
                                    memories.append(
                                        {
                                            "role": "user",
                                            "content": result,
                                            "name": "openLink tool"
                                        }
                                    )
                                if tool["name"] == "analyseImage":
                                    result = analyseImage( tool["params"]["source"], tool["params"]["prompt"], tool["params"]["renew"] )
                                    memories.append(
                                        {
                                            "role": "user",
                                            "content": result,
                                            "name": "analyseImage tool"
                                        }
                                    )
                                if tool["name"] == "openApp":
                                    result = openApp( tool["params"]["app"] )
                                    memories.append(
                                        {
                                            "role": "user",
                                            "content": result,
                                            "name": "openApp tool"
                                        }
                                    )
                                if tool["name"] == "getLocalisation":
                                    result = getLocalisation()
                                    memories.append(
                                        {
                                            "role": "user",
                                            "content": result,
                                            "name": "getLocalisation tool"
                                        }
                                    )
                                if tool["name"] == "notUnderstand":
                                    raise MyException( "the llm didn't undersand (not undestand tool)" )
                                if tool["name"] == "sleepSystem":
                                    sleepSystem = True
                            
                            active_tools = [
                                "analyseImage",
                                "getLocalisation"
                            ]
                            need_response = False
                            for tool in used_tools:
                                if tool["name"] in active_tools:
                                    need_response = True
                                    break

                            if need_response:
                                output, content = Rika()
                            else:
                                content["tools"] = []



                        question = ""

                        # print( f"{memory=}" )
                        # print( f"{memories=}" )

                        # print( "calc 4" )
                        if sleepSystem:
                            print( "Saving memory..." )
                            Json.write( memories, "memory.json" )
                            break

                    # except TypeError as e:
                    #     pass
                    except MyException:
                        pass
    except KeyboardInterrupt:
        print( "Saving memory..." )
        Json.write( memories, "memory.json" )
        System.clear()
        print( "exiting..." )
        exit( 0 )