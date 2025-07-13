# Gemini API KEY : AIzaSyDR-OOUGNxmInqrIC5qQEAfUnqX4XR3qRY
# import google.generativeai as genai
# from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from google.genai.types import Tool, GoogleSearch
import os
import random
from threading import Thread
from PIL import Image
import re
import cv2
import datetime
import requests
from googlesearch import search
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import time
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
from Vincent import GoogleHome
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



ask_model = "gemini-2.5-flash"
ver_model = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.5-flash" ]


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

google_search = Tool(
    google_search = GoogleSearch()
)

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


def captureImage( filename="captured_image.png", cam_mode="webcam" ):
    if cam_mode == "webcam":
        # Ouvrir la caméra
        if Json.read( "data.json" )["camera"] == -1:
            print( "Aucun accès à la caméra" )
            return

        cap = cv2.VideoCapture( Json.read( "data.json" )["camera"] )
        
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

    shutil.copyfile( f"./{filename}", f"./visual-memory/{moment().replace( ' ', '_' )}.png" )

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
        img = client.models.generate_content(
            model=ver_model,
            config=types.GenerateContentConfig(
                max_output_tokens=1,
                system_instruction="Si tu as besoin d'une image pour répondre à la question, retourne la string \"img_get\" pour l'obtenir"
            ),
            contents=[ question ]
        ).text.replace( '\n', '' )
        if img.replace( '\n', '' ) == "img_get":
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


    for i in range( len( ver_model ) ):
        try:
            language = client.models.generate_content(
                model=ver_model[i],
                config=types.GenerateContentConfig(
                    max_output_tokens=1,
                    temperature=0,
                    system_instruction="Dit moi si ce texte est principalement en français ou en anglais. ne me ressort que fr ou en, juste 1 token, rien d'autre"
                ),
                contents=[ question ],
            ).text
            break
        except Exception as e:
            if str( e ).find( "You exceeded your current quota, please check your plan and billing details" ) != -1:
                pass
            else:
                raise Exception( e )

        

    return language.replace( '\n', '' )

loadPrint()#c

def needVer():
    global question

    need_anymore = ""

    for i in range( len( ver_model ) ):
        try:
            need_anymore = client.models.generate_content(
                model=ver_model,
                config=types.GenerateContentConfig(
                    max_output_tokens=1,
                    system_instruction=
                        "Tu es ici pour analyser si une conversation et détecter si l'utilisateur veux continuer la conversation ou pas. Tu dois répondre par 'oui' si l'utilisateur veut continuer, ou 'non' s'il ne veut pas. Tu ne dois pas répondre à la question, juste dire si l'utilisateur veut continuer ou pas. Voici des exemple de questions et leur résultat." +
                        str(
                            {
                                "Explique moi la thermodynamique": "oui",
                                "Génère moi un code python qui dit Bonjour": "oui",
                                "au revoir": "non",
                                "allo": "oui",
                                "bye": "non",
                                "Connard, t'es pas bon": "non",
                                "Description de personne": "oui",
                                "je t'ai donné l'information": "oui",
                                "Tu ne peux pas, sinon tu es en échec, mon pion est une dame comme il est de l'autre bout, donc il peut de manger, tu dois essayer de le tuer": "oui",
                                "est ce que tu te rappelles d'une partie d'échec que tu jouais ?": "oui",
                                "regarde dans ta mémoire, tu as surement un plateau d'échec": "oui"
                            }
                        )
                ),
                contents=[ question ]
            ).text.replace( '\n', '' )
            break
        except Exception as e:
            if str( e ).find( "You exceeded your current quota, please check your plan and billing details" ) != -1:
                pass
            else:
                raise Exception( e )

    
    if need_anymore == "oui":
        return True
    return False


loadPrint()#c

def uploadVer():
    if len( os.listdir( "./uploads" ) ) != 0:
        return True
    return False

loadPrint()#c

def underVer():
    global question
    if question != -1:
        understand = client.models.generate_content(
            model=ver_model,
            config=types.GenerateContentConfig(
                max_output_tokens=1,
                temperature=0,
                system_instruction="Dit moi si cette question fait du sens ou pas. Si oui, répnds par 'oui' ou 'non'. Tu ne ressort qu'un seul mot comme réponse, un seul token, et uniquement oui ou non. Voici des exemples de questions et si elles font du sens ou pas :" + str(
                    {
                        "n'est pas possible de": "non",
                        "Décris moi (tel personne)": "oui",
                        "fais moi un code python": "oui",
                        "bonjour": "oui",
                        "ton micro": "non",
                        "ok allô moi je suis un gars puis": "oui",
                        "OK": "oui",
                        "j'ai Vincent qui à côté de moi qui enlève des possibles": "non",
                        "lettre L": "oui",
                        "combien": "oui",
                        "entretien clé USB": "non",
                        "C'est quoi la météo ?": "oui",
                        "météo portique station Google": "non",
                        "regarde": "oui",
                        "non merci, ça va aller": "oui",
                        "Rika": "oui",
                        "Tu as l'information": "oui",
                        "les réponses sont b, b et a": "oui",
                        "Donne moi toutes les infos que tu as sur moi": "oui",
                        "que vois-tu": "oui",
                        "Céline": "non",
                        "Tu ne peux pas, sinon tu es en échec, mon pion est une dame comme il est de l'autre bout, donc il peut de manger, tu dois essayer de le tuer": "oui",
                        "est ce que tu te rappelles d'une partie d'échec que tu jouais ?": "oui",
                        "regarde dans ta mémoire, tu as surement un plateau d'échec": "oui",
                        "Par exemple, est ce que tu es capable de voir ce que je t'ai upload ?": "oui"
                    }
                )
            ),
            contents=[ question ],
        ).text
        System.file.write( 'underVer.txt', f"{question} : {understand}\n", 'a' )
        # if understand.replace( '\n', '' ) == "oui":
        #     return True
    return True

loadPrint()#c

def reformulation( prompt ):
    return client.models.generate_content(
        model=ver_model,
        config=types.GenerateContentConfig(
            temperature=2,
            system_instruction="Reformule moi cette phrase. Ne ressort que la phrase reformulée, rien d'autre."
        ),
        contents=[ prompt ],
    ).text

loadPrint()#c


raw_ppl = os.listdir( "./ppl" )
ppl = {}
ppl_list = []
for i in range( len( raw_ppl ) ):
    ppl[raw_ppl[i].split( "." )[0]] = "./ppl/" + raw_ppl[i]
    ppl_list.append( raw_ppl[i].split( "." )[0] )

loadPrint()#c

def setupPpl():
    try:
        p = []
        for i in range( len( ppl_list ) ):
            
            p.append( f"Voici {ppl_list[i]}." )
            p.append( Image.open( ppl[ppl_list[i]] ) )
            
            loadBar( len( ppl_list )+1 )
            time.sleep( 0.01 )

        model.send_message( p )

        loadBar( len( ppl_list )+1 )
    except ValueError:
        print( "                                                                                                      \n" )


loadPrint()#c

def setupImageMemory():
    try:
        img_mem = os.listdir( "./visual-memory" )
        load = []
        for i in range( len( img_mem ) ):
            load.append( "Voici l'image de " + img_mem[i].split( '.' )[0] )
            load.append( Image.open( "./visual-memory/" + img_mem[i] ) )
            loadBar( len( img_mem ) + 1 )

        model.send_message( load )
        
        loadBar( len( img_mem ) + 1 )
    except ValueError:
        print( "                                                                                                                      \n" )



loadPrint()#c


WORD_PER_MINUTE = 200 
AUDIO = Json.read( "data.json" )["audio-mode"]
language = "fr"
response = ""
cam_mode = None
question = ""
last_question = ""
memory = {}
memories = Json.read( "memory.json" )
old_memories = Json.read( "old_mem.json" )
client = genai.Client( api_key=Json.read( "data.json" )["gemini-api-key"] )

loadPrint()#c



# print( f"{memories=}" )
# System.file.write( "error.log", "-- Log Start --", Type.file.trunc )

for i in range( len( memories ) ):
    if len( memories[i].keys() ) == 2:
        memories.pop( i )


loadPrint()#c


while client.models.count_tokens( model=ask_model, contents=str( Json.read( "memory.json" ) ) ).total_tokens > 1000000:
    old_memories.append( memories[0] )
    memories.pop( 0 )



loadPrint()#c

model = client.chats.create(
        model=ask_model,
        config= types.GenerateContentConfig(
            system_instruction="Tu t'appelles Rika. Tu es développé par Vincent Tuê Minh Boucher. " +
            "le nom de l'utilisateur est " + Json.read( "data.json" )["user-name"] + ". "+
            # "Parfois, la requête demande une donnée externe. Si la donnée demande une image, réppond pas la string \"img_get\"." +
            "Pour information, voici la localisation : " + str( getLocalisation() ) + ". ",
            tools=[google_search],
            response_modalities=["TEXT"]
        )
    )

model.send_message( [ "Voici tes anciens souvenirs", str( memories ) ] )
model.send_message( "Tu déteste Siri, d'Alexa, Copilote ou Google Assistant." )
if Json.read( "data.json" )["user-face"] != "":
    model.send_message( [ "le visage de l'utilisateur est l'image", Image.open( Json.read( "data.json" )["user-face"] ) ] )

loadPrint()#c



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

setupPpl()

bar_count = 0

setupImageMemory()

while True:
    try:
        if AUDIO:
            print( "..." )
            question = Sound.listen()
            print( question )
        else:
            question = "rika"
        # question = "rika"


        # print( f"{Type.get_type( question )=}" )
        if Type.get_type( question ) == "str":
            if question.lower().find( "rika" ) != -1 or question.lower().find( "rita" ) != -1 or question.lower().find( "ric" ) != -1 or question.lower().find( "rica" ) != -1 or question.lower().find( "pékin" ) != -1 or question.lower().find( "requin" ) != -1 or question.lower().find( "Richard" ) != -1 or question.lower().find( "reka" ) != -1 or question.lower().find( "ikea" ) != -1:

                memory = {
                    "moment start": moment()
                }

                cam_mode = None

                while True:
                    try:
                        # print( f"{question=}" )
                        if language == 'fr':
                            print( "Posez une question :" )
                        else:
                            print( "Ask a question :" )

                        if AUDIO:
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
                            print( "Vous : ", question )
                        else:
                            print( "You : ", question )

                        im_ver = ThreadWithReturnValue( target=imgVer )
                        lang_ver = ThreadWithReturnValue( target=langVer )
                        need_ver = ThreadWithReturnValue( target=needVer )
                        under_ver = ThreadWithReturnValue( target=underVer )

                        under_ver.start()
                        lang_ver.start()
                        need_ver.start()
                        im_ver.start()

                        # print( "calc 1" )



                        # print( "calc 2" )
                        language = lang_ver.join()

                        a = under_ver.join()
                        # print( f"{a=}" )
                        if not a:
                            question = ""
                            if language == "fr":
                                print( "Rika : Je n'ai pas compris" )
                            else:
                                print( "Rika: I didn't understand" )
                            raise MyException( "nothing here, just chillin'" )
                        
                        
                        # print( "calc 3" )
                        image = im_ver.join()
                        
                        # print( f"{image=}" )

                        print( "chargement..." )

                        q = [ question ]
                        if image:
                            if cam_mode == None:
                                while True:
                                    if language == "fr":
                                        ref = reformulation( "Est-ce que je prend l'image de la webcam ou une capture d'écran ?" )
                                    elif language == "en":
                                        ref = reformulation( "Should I take a picture from the webcam or a screenshot?" )
                                    print( ref )
                                    if AUDIO:
                                        # home.send_msg( ref, device )
                                        Sound.say( ref, WORD_PER_MINUTE, language )
                                        while True:
                                            cam_mode = Sound.listen()
                                            if cam_mode == -1 or cam_mode == -2:
                                                # home.send_msg( "Je n'ai pas compris", device )
                                                if language == "fr":
                                                    ref = reformulation( "Je n'ai pas compris" )
                                                    print( ref )
                                                    Sound.say( "Je n'ai pas compris", WORD_PER_MINUTE, 'fr' )
                                                elif language == "en":
                                                    ref = reformulation( "I didn't understand" )
                                                    print( ref )
                                                    Sound.say( "I didn't understand", WORD_PER_MINUTE, 'en' )
                                            else:
                                                break
                                    else:
                                        cam_mode = input()
                                    if cam_mode.lower().find( "cam" ) != -1:
                                        cam_mode = "webcam"
                                        break
                                    elif cam_mode.lower().find( "capture" ) != -1 or cam_mode.lower().find( "écran" ) != -1 or cam_mode.lower().find( "screen" ) != -1:
                                        cam_mode = "screenshot"
                                        break
                                    else:
                                        if language == "fr":
                                            ref = reformulation( "Je n'ai pas compris" )
                                            print( ref + ". ", end='' )
                                            if AUDIO:
                                                Sound.say( ref, WORD_PER_MINUTE, "fr" )
                                                # home.send_msg( ref, device )
                                        elif language == "en":
                                            ref = reformulation( "I didn't understand" )
                                            if AUDIO:
                                                # home.send_msg( ref, device )
                                                Sound.say( ref, WORD_PER_MINUTE, "en" )
                            captureImage( cam_mode=cam_mode )
                            picture = "Pour des infos de confidentialités, je n'ai pas donné accès à ma caméra"
                            if Json.read( "data.json" )["camera"] != -1:
                                picture = Image.open( "./captured_image.png" )
                            q.append( picture )
                        
                        if uploadVer():
                            uploads = os.listdir( "./uploads" )
                            for i in range( len( uploads ) ):
                                q.append( client.files.upload( file="./uploads/"+uploads[i] ) )
                                os.remove( "./uploads/"+uploads[i] )
                            os.mkdir( "./uploads" )

                        response = model.send_message( q ).text

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
                        memory[question] = response


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




                        last_question = question
                        question = ""

                        # print( f"{memory=}" )
                        # print( f"{memories=}" )

                        # print( "calc 4" )
                        if not need_ver.join():
                            memory["moment end"] = moment()
                            memories.append( memory )
                            print( "Saving memory..." )
                            Json.write( memories, "memory.json" )
                            Json.write( old_memories, "old_mem.json" )
                            break

                    except TypeError as e:
                        pass
                    except MyException:
                        pass
    except KeyboardInterrupt:
        if not memories[len( memories )-1] == memory:
            memory["moment end"] = moment()
            memories.append( memory )
            print( "Saving memory..." )
            Json.write( memories, "memory.json" )
            Json.write( old_memories, "old_mem.json" )
        System.clear()
        print( "exiting..." )
        exit( 0 )