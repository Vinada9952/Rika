from pygrabber.dshow_graph import FilterGraph
from email.utils import parsedate_to_datetime
from email.header import decode_header
from email.mime.text import MIMEText
from json import JSONDecodeError
from groq import APIStatusError
import speech_recognition as sr
from plyer import notification
from shazamio import Shazam
import soundfile as sf
from PIL import Image
from groq import Groq
import pyaudiowpatch
from gui import GUI
import numpy as np
import webbrowser
import subprocess
import threading
import tempfile
import requests
import edge_tts
import keyboard
import datetime
import asyncio
import smtplib
import logging
import imaplib
import base64
import pygame
import random
import email
import glob
import json
import math
import time
import cv2
import sys
import mss
import os
import re

from web.server import VOICE

GUI.startGUI()

GUI.setInit( True )

os.system( "cls" )
load_print = 0

load_number = -1

def loadPrint():
    global load_number
    global load_print
    # return
    def read( file_name: str ):
        return_file = []
        try:
            file = open( file_name, 'r', encoding="utf-8" )
            brut_file = file.read()+'\n'
            file.close()
            traitement = ''
            for i in range( len( brut_file ) ):
                for j in range( len( brut_file[i] ) ):
                    if brut_file[i][j] == '\n':
                        return_file.append( traitement )
                        traitement = ''
                    else:
                        traitement += brut_file[i][j]
            return return_file
        except FileNotFoundError:
            return FileNotFoundError

    load_print += 1
    # f = '\n'.join( read( "C:/Users/" ) )
    if load_number == -1:
        f = '\n'.join( read( __file__ ) )
        count = f.count( "loadPrint()#c" )-1
        load_number = count
    else:
        count = load_number

    bar = '[' + ( '.'*100 ) + ']'


    for i in range( int( load_print*100/count ) ):
        bar = bar.replace( '.', '#', 1 )

    percentage = load_print*100/count

    GUI.setLoading( percentage )

    print( bar, f"{load_print}/{count}", end='\r' )
    if load_print == count:
        print( "\n" )
        GUI.setInit( False )

loadPrint()#c

class ExitAgent( Exception ):
    pass

loadPrint()#c

class NotValidResponse( Exception ):
    pass

loadPrint()#c

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

loadPrint()#c

class ThreadWithReturnValue( threading.Thread ):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

loadPrint()#c

class Substitute:
    def join(self, *args, **kwargs):
        return

loadPrint()#c

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
        text = "   " + text.replace( '*', '' ).replace( '\n', ".     " )
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

loadPrint()#c

def april_fools_rickroll():
    today = datetime.datetime.now()
    
    if today.day == 1 and today.month == 4:
        try:
            subprocess.Popen( ["curl", "ASCII.live/rick"], creationflags=subprocess.DETACHED_PROCESS, shell=True)
            if AUDIO:
                Sound.generateVoice( "Activation du protocol April Fools", VOICE )
                Sound.playVoice()
        except Exception as e:
            print("Erreur lors de l'exécution de curl :", e)

loadPrint()#c

def _get_apps_windows() -> list[dict]:
    search_dirs = SEARCH_DIRS

    seen = set()
    apps = []

    for d in search_dirs:
        if not d or not os.path.isdir(d):
            continue
        for exe in glob.glob(os.path.join(d, "**", "*.exe"), recursive=True):
            name = os.path.splitext(os.path.basename(exe))[0]
            if name in seen:
                continue
            seen.add(name)
            apps.append({"name": name, "path": exe})

    return sorted(apps, key=lambda x: x["name"].lower())

loadPrint()#c

# ── macOS ─────────────────────────────────────────────────────────────────────

def _get_apps_macos() -> list[dict]:
    apps = []
    search_dirs = ["/Applications", os.path.expanduser("~/Applications")]

    for directory in search_dirs:
        if not os.path.isdir(directory):
            continue
        for entry in os.scandir(directory):
            if not entry.name.endswith(".app"):
                continue

            name = entry.name.removesuffix(".app")
            macos_dir = os.path.join(entry.path, "Contents", "MacOS")
            exe_path = entry.path  # fallback = le bundle .app

            if os.path.isdir(macos_dir):
                for exe in os.scandir(macos_dir):
                    if os.access(exe.path, os.X_OK):
                        exe_path = exe.path
                        break

            apps.append({"name": name, "path": exe_path})

    return sorted(apps, key=lambda x: x["name"].lower())

loadPrint()#c

# ── Linux ─────────────────────────────────────────────────────────────────────

def _get_apps_linux() -> list[dict]:
    import configparser

    apps = []
    seen = set()
    desktop_dirs = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        os.path.expanduser("~/.local/share/applications"),
        "/var/lib/snapd/desktop/applications",
        "/var/lib/flatpak/exports/share/applications",
        os.path.expanduser("~/.local/share/flatpak/exports/share/applications"),
    ]

    for directory in desktop_dirs:
        if not os.path.isdir(directory):
            continue
        for entry in os.scandir(directory):
            if not entry.name.endswith(".desktop"):
                continue

            config = configparser.ConfigParser(strict=False)
            try:
                config.read(entry.path, encoding="utf-8")
            except Exception:
                continue

            if "Desktop Entry" not in config:
                continue

            section = config["Desktop Entry"]
            if section.get("NoDisplay", "false").lower() == "true":
                continue
            if section.get("Type", "") != "Application":
                continue

            name = section.get("Name", "").strip()
            exec_cmd = section.get("Exec", "").strip()

            if not name or name in seen:
                continue

            exe_path = exec_cmd.split("%")[0].strip().split()[0] if exec_cmd else ""
            seen.add(name)
            apps.append({"name": name, "path": exe_path})

    return sorted(apps, key=lambda x: x["name"].lower())

def getAllApps() -> list[dict]:
    """
    Retourne la liste de toutes les applications installées sur l'ordinateur.
    Compatible Windows, macOS et Linux.

    Returns:
        list[dict]: Liste de dicts avec les clés 'name' et 'path'.
    """
    platform = sys.platform

    if platform == "win32":
        return _get_apps_windows()
    elif platform == "darwin":
        return _get_apps_macos()
    else:
        return _get_apps_linux()

loadPrint()#c

logs = []
def log( message, info, level ):
    logs.append(
        {
            "level": level,
            "message": message,
            "info": info
        }
    )
    Json.write( logs, "log.log" )

loadPrint()#c

# =====================
# CONFIG
# =====================

settings = Json.read( "settings.json" )

loadPrint()#c

API_KEYS = settings["api"]["api-keys"]
clients = [
    Groq( api_key=n )
    for n in API_KEYS
]
del API_KEYS

loadPrint()#c

call_names = settings["call"]["names"]
CALL_HOTKEY = settings["call"]["hotkey"]

loadPrint()#c

MAIN_MODEL = settings["models"]["main"]
VISION_MODEL = settings["models"]["vision"]
ASK_MODEL = settings["models"]["data"]
WEB_MODEL = settings["models"]["web"]
MAX_RETRIES = settings["api"]["max-api-retries"]
ASSISTANT_NAME = settings["assistant-name"]

loadPrint()#c

AUDIO = settings["audio"]["audio"]
VOICE = settings["audio"]["voice"]
AUDIO_DURATION_LIMIT = settings["audio"]["audio-duration-threshold"]

loadPrint()#c

SCREENSHOT_DIR = settings["directories"]["screenshots"]
WEBCAM_PATH = settings["directories"]["webcam"]

loadPrint()#c

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

SAMPLE_RATE            = 44100
DURATION               = 8
TIMEOUT                = 12
SPEAKER_SILENCE_THRESH = 0.005
MIC_SILENCE_THRESH     = 0.0005  # beaucoup plus sensible que le speaker
MIC_GAIN               = 5.0     # multiplie le volume du micro (augmente si encore trop faible)

loadPrint()#c

SMTP_SERVER = settings["email"]["smtp"]["server"]
SMTP_PORT = settings["email"]["smtp"]["port"]
EMAIL = settings["email"]["email"]
EMAIL_PASSWORD = settings["email"]["pwd"]
IMAP_SERVERS = {
    "gmail.com":      ("imap.gmail.com", 993),
    "googlemail.com": ("imap.gmail.com", 993),
    "outlook.com":    ("imap-mail.outlook.com", 993),
    "hotmail.com":    ("imap-mail.outlook.com", 993),
    "live.com":       ("imap-mail.outlook.com", 993),
    "msn.com":        ("imap-mail.outlook.com", 993),
    "yahoo.com":      ("imap.mail.yahoo.com", 993),
    "yahoo.fr":       ("imap.mail.yahoo.com", 993),
    "icloud.com":     ("imap.mail.me.com", 993),
    "me.com":         ("imap.mail.me.com", 993),
}

loadPrint()#c

SEARCH_DIRS = []
for element in settings["directories"]["apps-path"]["get-env"]:
    SEARCH_DIRS.append(
        os.environ.get(
            element["key"],
            element["default"]
        )
    )
for element in settings["directories"]["apps-path"]["expand-user"]:
    SEARCH_DIRS.append(
        os.path.expanduser( element )
    )
for element in settings["directories"]["apps-path"]["normal"]:
    SEARCH_DIRS.append( element )

loadPrint()#c

USERNAME = settings["email"]["user-email"]["name"]
USER_EMAIL = settings["email"]["user-email"]["email"]
CONTACT_LIST = Json.read( settings["directories"]["contacts"] )

loadPrint()#c

SERVER_URL = settings["server"]["url"]
SET_CONVERSATION = settings["server"]["set-conversation"]
GET_CONVERSATION = settings["server"]["get-conversation"]

loadPrint()#c

PROTOCOLS = [ { "name": settings["reset-protocol-name"], "command": "/delete-memory" } ] + Json.read( settings["directories"]["protocols"] )

protocol_list = ''
for protocol in PROTOCOLS:
    protocol_list += f"\n    -> {protocol["name"]}"

loadPrint()#c

def getAllAppsThread():
    global APPLICATIONS
    APPLICATIONS = getAllApps()
    sendNotification( "Applications chargées.", "Scan des applications installés terminées" )

get_all_apps_thread = threading.Thread( target=getAllAppsThread )
get_all_apps_thread.start()

loadPrint()#c

treating_response = Substitute()

loadPrint()#c

names = []
for contact in CONTACT_LIST:
    name = contact["name"]
    relation = contact["relation"]
    language = contact["language"]
    names.append( f"    -> {name} ({relation}) - Langue parlé : {language}" )

CONTACT_NAMES = '\n'.join( names )

loadPrint()#c

conversation = Json.read( "./conversation.json" )
if SERVER_URL:
    data = requests.get( f"{SERVER_URL}/{GET_CONVERSATION}" )
    conversation = data.json()
    del data
# data = Json.read( "./conversation.json" )
# print( data )
# print( data.json() )
# conversation = data.json()["conversation"]
# print( conversation  )

loadPrint()#c

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
{'{'}
  "message": "ce que tu dis à l'utilisateur",
  "tools": []
{'}'}

Cas avec action(s) :

{'{'}
  "message": "ce que tu dis à l'utilisateur",
  "tools": [
    {'{'}
      "name": "openLink",
      "params": {'{'}
        "link": "https://www.google.com/search?q=latest+news+about+ai"
      {'}'}
    {'}'},
    {'{'}
      "name": "analyseImage",
      "params": {'{'}
        "source": "screenshot",
        "prompt": "Décris ce que tu vois sur tous les écrans"
      {'}'}
    {'}'}
  ]
{'}'}

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
  - ouvrir une application
  - params:
    -> app (string): application à ouvrir

- openLink
  - UTILISATION OBLIGATOIRE si l'utilisateur demande un lien
  - Avant de l'utiliser, vérifie toi-même sur internet si le lien fonctionne
  - params:
    -> query (string): Description du lien (ex: dernière vidéo de mon youtuber préféré)
  - exemples de cas d'utilisation:
    -> Je veux voir une vidéo youtube
    -> trouve moi les scores des olympiques
    -> trouve moi une carte de Montréal

- sendEmail
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

- doProtocol
  - Utiliser un des protocols prévu
  - À utiliser uniquement quand je te demande explicitement
  - params:
    -> protocol (string): Nom du protocol
  - liste de protocol:{protocol_list}

- saveFile
  - Sauvegarder un fichier texte
  - À utiliser pour sauvegarder un fichier texte, un gros contenu texte ou un script
  - Donne toujours le résultat d'une réponse, qui n'est pas simplement une information ou la confirmation d'un outil, dans l'outil saveFile
  - params:
    -> name (string): Nom du fichier
    -> content (string): Contenu du fichier
  - exemple d'utilisation:
    -> Fait moi un script...
    -> Écrit moi un poème...
    -> Fait moi un rapport...
    -> Affiche moi un résumé...
  
- webSearch
  - Faire une recherche sur le web
  - params:
    -> query (string): Ce que tu veux savoir
  - Tu peux l'utiliser à n'importe quel moment, sans avoir besoin d'autorisation

- recognizeMusic
  - Reconaitre la musique qui joue

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
- À la fin de chaque email, signe ton nom et met une formule de politesse
- Dans les email, met le courriel dans la langue parlé du destinataire
- Ne dis JAMAIS les paramètres utilisés pour les outils.
- Ne fait JAMAIS de résumé de conversation, sauf quand je te le demande.
- Si une action est requise (ex: envoyer un email, ouvrir une app, ouvrir un lien, analyser une image), la réponse est invalide si aucun outil n'est appelé.
- Dès que tu reçois un email, dit le à l'utilisateur et un résumé de son contenu, et fait le pour chaque email. Si l'utilisateur n'a pas reçu d'email, n'en parle pas
- Il est INTERDIT de simuler une action dans le message sans appeler l'outil correspondant.
- Si une action est nécéssaire, ne te contente pas juste de répondre, FAIT l'action
- Ne met pas de mise en page ou des choses dans le genre pour faire des tableaux, titres en gras, ressort un texte simple destiné à être affiché dans le terminal
- Essaie de faire les messages les plus courts possibles
- Ta réponse est fait pour être dite à l'oral. Garde des caractères normaux pouvant être dit par un module TTS. C'est à dire, ne met pas de parenthèses et autres trucs du genre
"""

conversation[0] = {
    "role": "system",
    "name": "instructions",
    "content": base_message
}

loadPrint()#c

# =====================
# SETUP
# =====================
for file in os.listdir( SCREENSHOT_DIR ):
    os.remove( os.path.join( SCREENSHOT_DIR, file ) )
os.makedirs( SCREENSHOT_DIR, exist_ok=True )

loadPrint()#c

def get_camera_index( search ):

    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate( devices ):
        available_cameras[device_index] = device_name

    for index, name in available_cameras.items():
        if name.find( search ) != -1:
            return index

    return -1


loadPrint()#c

called = False
audio_tmp = AUDIO
def toggleRika():
    global called, AUDIO
    print( f"{ASSISTANT_NAME} Called" )
    # GUI.forceTopMost()
    called = True
    AUDIO = False

loadPrint()#c

def checkAudioCall():
    global called
    while True:
        # print( f"check if called by audio : {called=}" )
        if not called:
            print( "..." )
            question = Sound.listen()

            if type( question ) == str:
                calls = question.lower().split( ' ' )
                for call_name in call_names:
                    for call in calls:
                        if call.find( call_name.lower() ) != -1:
                            called = True
                            break
                    if called:
                        break
            if not called:
                print( question )
            if called:
                print( ASSISTANT_NAME )
        time.sleep( 1 )

check_audio_call = threading.Thread( target=checkAudioCall )

loadPrint()#c

def sendNotification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='MonApp',
        timeout=3
    )

loadPrint()#c

class Model:
    def askModel( model: str, message: dict, thinking: str, max_retries: int, verification ):
        global clients
        can_think = True
        for i in range( max_retries ):
            try:
                if can_think:
                    ans = random.choice( clients ).chat.completions.create(
                        model=model,
                        messages=message,
                        reasoning_effort=thinking
                    ).choices[0].message.content
                else:
                    ans = random.choice( clients ).chat.completions.create(
                        model=model,
                        messages=message
                    ).choices[0].message.content
                if not verification( ans ):
                    raise NotValidResponse( f"The ai's response doesn't match or respect the output specifications. Verification : {verification.name()}, response is {ans}" )
                return ans
            except APIStatusError as e:
                print( str( e ) )
                if str( e ).find( "reasoning_effort" ) != -1 and str( e ).find( "not supported" ) != -1:
                    can_think = False
                if e.status_code == 413 and str( e ).lower().find( "request too large for model" ) != -1:
                    autoEraseConversation()
            except NotValidResponse as e:
                print( str( e ) )
                log( f"Invalid response from AI: {ans}", str( e ), "error" )
    
    class Verification:
        def isJson( object ):
            def name():
                return "isJson"
            try:
                json.loads( object )
                return True
            except JSONDecodeError:
                return False
        
        def isPath( path ):
            def name():
                return "isPath"
            return os.path.exists( path )

        def isLink( link ):
            def name():
                return "isLink"
            if link.find( "http" ) == 0:
                return True
            if link.find( "www" ) != -1:
                return True
        
        def rawResponse( a ):
            def name():
                return "rawResponse"
            return True


loadPrint()#c

# =====================
# IMAGE TO BASE64
# =====================
def image_to_base64( path ):
    with open( path, "rb" ) as f:
        return base64.b64encode( f.read() ).decode()

loadPrint()#c

def webSearch( query: str ):
    result = Model.askModel(
        WEB_MODEL,
        [
            {
                "role": "system",
                "content": """
Va chercher sur internet la réponse à la question de l'utilisateur.
"""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "high",
        MAX_RETRIES,
        Model.Verification.rawResponse
    )
    return result, True

loadPrint()#c

def rms(audio: np.ndarray) -> float:
    return float(np.sqrt(np.mean(audio ** 2)))

loadPrint()#c

def get_default_wasapi_loopback_device(p: pyaudiowpatch.PyAudio) -> dict | None:
    try:
        return p.get_default_wasapi_loopback()
    except Exception as e:
        pass

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev.get("isLoopbackDevice", False):
            return dev

    return None

loadPrint()#c

def _record_worker(device_index: int, sample_rate: int, channels: int,
                   duration: int, result_holder: list, error_holder: list) -> None:
    """Enregistrement dans un thread séparé avec sa propre instance PyAudio."""
    p = pyaudiowpatch.PyAudio()
    try:
        frames = []
        stream = p.open(
            format=pyaudiowpatch.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=1024,
        )

        num_chunks = int(sample_rate / 1024 * duration)
        for _ in range(num_chunks):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        raw   = b"".join(frames)
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

        if channels == 2:
            audio = audio.reshape(-1, 2).mean(axis=1)

        if sample_rate != SAMPLE_RATE:
            try:
                from scipy.signal import resample_poly
                from math import gcd
                g = gcd(SAMPLE_RATE, sample_rate)
                audio = resample_poly(audio, SAMPLE_RATE // g, sample_rate // g)
            except ImportError:
                new_len = int(len(audio) * SAMPLE_RATE / sample_rate)
                audio = np.interp(
                    np.linspace(0, len(audio) - 1, new_len),
                    np.arange(len(audio)),
                    audio
                )

        result_holder.append(audio)

    except Exception as e:
        error_holder.append(str(e))
    finally:
        p.terminate()

loadPrint()#c

def record_with_timeout(device_index: int, sample_rate: int, channels: int,
                        duration: int, label: str) -> np.ndarray | None:
    """Lance l'enregistrement dans un thread avec un timeout strict."""
    result_holder = []
    error_holder  = []

    t = threading.Thread(
        target=_record_worker,
        args=(device_index, sample_rate, channels, duration, result_holder, error_holder),
        daemon=True,
    )
    t.start()
    t.join(timeout=TIMEOUT)

    if t.is_alive():
        return None

    if error_holder:
        return None

    return result_holder[0] if result_holder else None

loadPrint()#c

def record_loopback(device_info: dict, duration: int = DURATION) -> np.ndarray | None:
    sample_rate = int(device_info["defaultSampleRate"])
    channels    = min(int(device_info["maxInputChannels"]), 2)
    dev_index   = int(device_info["index"])

    return record_with_timeout(dev_index, sample_rate, channels, duration, "speaker")

loadPrint()#c

def record_default_mic(duration: int = DURATION) -> np.ndarray | None:
    p = pyaudiowpatch.PyAudio()
    try:
        dev_info    = p.get_default_input_device_info()
        sample_rate = int(dev_info["defaultSampleRate"])
        dev_index   = int(dev_info["index"])
    except Exception as e:
        return None
    finally:
        p.terminate()

    audio = record_with_timeout(dev_index, sample_rate, 1, duration, "micro")
    if audio is not None:
        audio = np.clip(audio * MIC_GAIN, -1.0, 1.0)
    return audio

loadPrint()#c

async def identify(audio: np.ndarray, label: str = "") -> dict | None:
    shazam = Shazam()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        sf.write(tmp_path, audio, SAMPLE_RATE)
        result = await shazam.recognize(tmp_path)
    finally:
        os.unlink(tmp_path)

    if result and result.get("matches"):
        return result
    return None

loadPrint()#c

def extract_track_info(result: dict) -> dict:
    track = result.get("track", {})

    name   = track.get("title", "Inconnu")
    artist = track.get("subtitle", "Inconnu")

    # Album
    sections = track.get("sections", [])
    album = "Inconnu"
    for section in sections:
        for meta in section.get("metadata", []):
            if meta.get("title", "").lower() == "album":
                album = meta.get("text", "Inconnu")

    # Genre
    genres_obj = track.get("genres", {})
    genre = genres_obj.get("primary", "Inconnu")

    # Année de publication
    publication = "Inconnu"
    for section in sections:
        for meta in section.get("metadata", []):
            if meta.get("title", "").lower() in ("released", "year", "année", "date de sortie"):
                publication = meta.get("text", "Inconnu")

    # Spotify URI — dans hub.providers
    spotify = "Inconnu"
    for provider in track.get("hub", {}).get("providers", []):
        if provider.get("type") == "SPOTIFY":
            for action in provider.get("actions", []):
                uri = action.get("uri", "")
                if uri.startswith("spotify:"):
                    spotify = uri
                    break

    return {
        "name":        name,
        "artist":      artist,
        "album":       album,
        "genre":       genre,
        "publication": publication,
        "spotify":     spotify,
    }

loadPrint()#c

async def _recognize_music_async() -> dict:
    speaker_audio = None
    mic_audio     = None
    output        = {"note": "aucune musique détectée"}

    # ── Étape 1 : Speaker par défaut Windows (loopback WASAPI) ────────────────
    p = pyaudiowpatch.PyAudio()
    loopback_device = get_default_wasapi_loopback_device(p)
    p.terminate()

    if loopback_device:

        speaker_audio = record_loopback(loopback_device)

        if speaker_audio is not None:
            level = rms(speaker_audio)

            if level > SPEAKER_SILENCE_THRESH:
                result = await identify(speaker_audio, "speaker")
                if result:
                    info = extract_track_info(result)
                    output = {**info, "note": "musique détectée par speaker"}
                    # Reconnu : sauvegarde et fin, micro ignoré
                    mic_audio = record_default_mic()
                    return output

    # ── Étape 2 : Microphone par défaut ───────────────────────────────────────
    mic_audio = record_default_mic()

    if mic_audio is not None:
        level = rms(mic_audio)

        if level > MIC_SILENCE_THRESH:
            result = await identify(mic_audio, "micro")
            if result:
                info = extract_track_info(result)
                output = {**info, "note": "musique détectée par micro"}
            else:
                output = {"note": "musique non reconnue"}


    return output

loadPrint()#c

def recognizeMusic() -> dict:
    """Point d'entrée public. Retourne un dict avec les infos de la musique détectée."""
    return str( asyncio.run(_recognize_music_async()) ), True

loadPrint()#c

# =====================
# TOOL: openLink
# =====================
def openLink( query: str ):
    link = Model.askModel(
        WEB_MODEL,
        [
            {
                "role": "system",
                "content": """
Ton role est de donner un lien web à entrer dans un navigateur.
Tu dois uniquement donner le lien web et rien d'autre.
Le lien que tu vas donner doit corresprondre le plus possible à la demande de l'utilisateur
"""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "high",
        MAX_RETRIES,
        Model.Verification.isLink
    )
    success = webbrowser.open( link )
    if success:
        return f"ouverture de {link} réussie", False
    return f"ouverture de {link} raté", True

loadPrint()#c

# =====================
# TOOL: openApp
# =====================
def launchApp( app ):
    subprocess.Popen( [app["path"]], creationflags=subprocess.DETACHED_PROCESS, shell=True)
    return "Application lancé avec succès"

loadPrint()#c

def searchApp( apps: list, name: str ):
    found = []
    for app in apps:
        for word in name.lower().split( ' ' ):
            if word in app["name"].lower():
                found.append( app )
                break
    return found

loadPrint()#c

def appPath( apps, app: str ):
    print( f"{apps=}" )
    for i in range( MAX_RETRIES ):
        path = Model.askModel(
            "llama-3.1-8b-instant",
            [
                {
                    "role": "system",
                    "content": f"""
Voici une liste d'applications :
{json.dumps(apps, indent=4, ensure_ascii=False)}
L'utilisateur va te donner un nom d'application, et tu dois UNIQUEMENT ressortir le nom de l'application.
Tu dois ressortir UNIQUEMENT le nom, rien d'autre.
Le nom de l'application doit correspondre à un des noms dans la liste avec la clé "name".
Les applications n'ont pas tout le temps le même nom, tu dois donc choisir l'application qui correspond le mieux à la demande de l'utilisateur, en te basant sur la liste d'applications que je t'ai donnée.
Ne ressort RIEN D'AUTRE que le nom, absolument rien d'autre, pas ton raisonnement, par tes doutes, uniquement un nom valide pour l'exécution de l'application demandée par l'utilisateur.
Si tu hésite entre plusieurs, donne uniquement UN nom entre ceux que tu hésites
"""
                },
                {
                    "role": "user",
                    "content": app
                }
            ],
            "high",
            MAX_RETRIES,
            Model.Verification.rawResponse
        )
        print( f"Found path: {path}" )
        found = False
        for i in range( len( apps ) ):
            if apps[i]["name"] == path:
                found = True
                return launchApp( apps[i] )
        if found:
            break
    return f"Impossible de trouver l'application {app}", True

loadPrint()#c

def openApp( app ):
    global get_all_apps_thread
    print( f"searching for {app}..." )
    get_all_apps_thread.join()
    get_all_apps_thread = Substitute()
    search = searchApp( APPLICATIONS, app )
    return appPath( search, app ), False
# def openApp( app: str ):
#     app = app.lower()
#     if app == "spotify":
#         os.system( "spotify.exe" )
#     if app == "teams":
#         os.system( "ms-teams.exe" )
#     if app == "discord":
#         os.system( f"{os.path.expanduser("~")}/AppData/Local/Discord/Update.exe --processStart Discord.exe" )
#     if app == "vs code":
#         os.system( "code.exe" )
#     if app == "minecraft":
#         os.system( f"{os.path.expanduser("~")}/Desktop/Minecraft.lnk" )
#     return f"ouverture de {app} réussie",  False
    # return f"Link opened successfully ( {link} )" if webbrowser.open( link ) else "No link opened"

# def runCommand():
#     subprocess.run

loadPrint()#c

def doProtocol( name ):
    global PROTOCOLS, conversation
    for i in range( len( PROTOCOLS ) ):
        if name == PROTOCOLS[i]["name"]:
            if PROTOCOLS[i]["command"] == "/delete-memory":
                conversation = [ conversation[0] ]
                sleepSystem( False )
                Sound.waitForVoiceToFinish()
                Sound.generateVoice( "Vous aurez besoin de relançer mon programme", VOICE )
                Sound.playVoice()
                Sound.waitForVoiceToFinish()
                sys.exit( 0 )
                print( "Veuillez relancer le programme..." )
                Sound.generateVoice( "Veuillez relancer le programme...", VOICE )
                Sound.playVoice()
            subprocess.Popen( PROTOCOLS[i]["command"].split( ' ' ), creationflags=subprocess.DETACHED_PROCESS, shell=True)
            break
    return f"protocol {name} execution success", False

loadPrint()#c

def autoEraseConversation():
    file_name = "conversation" + str(time.time()) + ".json"
    text = f"Votre historique est trop gros, nous allons l'effacer. Si vous voulez conserver certains éléments, le tout sera enregistré dans {file_name} dans votre dossier Téléchargements"
    print( text )
    GUI.setTextToDisplay( text )
    with open( f"{os.path.expanduser("~")}/Downloads/{file_name}", 'w', encoding="utf-8" ) as f:
        json.dump( conversation, f, indent=4, ensure_ascii=False )
    if AUDIO:
        Sound.waitForVoiceToFinish()
        Sound.generateVoice( text, VOICE )
        Sound.playVoice()
    doProtocol( settings["reset-protocol-name"] )


loadPrint()#c

def saveFile( name, content ):
    if os.path.exists( f"{os.path.expanduser("~")}/Downloads/{name}" ):
        return f"Le fichier {name} existe déjà", True
    file = open( f"{os.path.expanduser("~")}/Downloads/{name}", 'w' )
    file.write( content )
    file.close()
    subprocess.Popen( ["notepad", f"{os.path.expanduser("~")}/Downloads/{name}"], creationflags=subprocess.DETACHED_PROCESS, shell=True)
    # os.system( f"notepad {os.path.expanduser("~")}/Downloads/{name}" )
    return f"Le fichier {name} a bien été créé", False

loadPrint()#c

# =====================
# TOOL: getLocalisation
# =====================
# def getLocalisation():
#     try:
#         response = requests.get( "https://ipinfo.io/json" )
#         data = str( response.json() )
#         # print( "localisation saved" )
#         return data, True
#     except Exception as e:
#         return "Erreur pour obtenir la localisation", True

def getLocalisation() -> dict:
    """
    Retourne un dictionnaire avec :
      - ip_location      : position approximative via IP
      - windows_location : position précise via le service Windows (GPS/Wi-Fi)
      - comparison       : écart entre les deux sources
      - generated_at     : horodatage UTC
    """

    def _get_ip() -> dict:
        try:
            resp = requests.get(
                "http://ip-api.com/json/",
                params={"fields": "status,message,country,regionName,city,"
                                   "zip,lat,lon,isp,org,query"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != "success":
                raise ValueError(data.get("message", "Réponse inattendue"))
            return str(
                {
                    "method": "ip",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "ip_address": data.get("query"),
                    "isp": data.get("isp"),
                    "organisation": data.get("org"),
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "zip": data.get("zip"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "accuracy_note": "Précision typique : ville (~5-50 km)",
                }
            ), True
        except Exception as exc:
            return str({"method": "ip", "error": str(exc)}), True

    def _get_windows() -> dict:
        try:
            import win32com.client
        except ImportError:
            return str( {"method": "windows",
                    "error": "pywin32 non installé (pip install pywin32)"} ), True
        try:
            locator = win32com.client.Dispatch("Windows.Devices.Geolocation.Geolocator")

            access = locator.RequestAccessAsync()
            deadline = time.time() + 10
            while access.Status != 4 and time.time() < deadline:
                time.sleep(0.1)
            if access.Status == 4 and access.GetResults() != 0:
                return str( {"method": "windows", "error": "Accès à la localisation refusé"} ), True

            locator.DesiredAccuracy = 0
            locator.DesiredAccuracyInMeters = 10

            op = locator.GetGeopositionAsync()
            deadline = time.time() + 30
            while op.Status != 4 and time.time() < deadline:
                time.sleep(0.2)
            if op.Status != 4:
                return str( {"method": "windows", "error": "Délai dépassé (30 s)"} ), True

            pos   = op.GetResults()
            coord = pos.Coordinate
            geo   = coord.Point.Position

            accuracy = getattr(coord, "Accuracy", None)
            alt_acc  = getattr(coord, "AltitudeAccuracy", None)
            speed    = getattr(coord, "Speed",   None)
            heading  = getattr(coord, "Heading", None)
            src_map  = {0: "Unknown", 1: "Cellular", 2: "Satellite",
                        3: "WiFi", 4: "IPAddress", 5: "Default",
                        6: "Obfuscated", 7: "Other"}
            source = src_map.get(getattr(coord, "PositionSource", -1), "Unknown")

            return str(
                {
                    "method": "windows",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "latitude":            geo.Latitude,
                    "longitude":           geo.Longitude,
                    "altitude_m":          geo.Altitude if geo.Altitude != 0 else None,
                    "accuracy_m":          round(accuracy, 2) if accuracy else None,
                    "altitude_accuracy_m": round(alt_acc, 2)  if alt_acc  else None,
                    "speed_ms":            round(speed, 2)    if speed    else None,
                    "heading_deg":         round(heading, 1)  if heading  else None,
                    "position_source":     source,
                    "accuracy_note":       "Précision typique : GPS ~5 m, Wi-Fi ~15-40 m",
                }
            ), True
        except Exception as exc:
            return str( {"method": "windows", "error": str(exc)} ), True

    def _compare(ip: dict, win: dict) -> dict:
        if "error" in ip or "error" in win:
            return str( {"note": "Comparaison impossible (données manquantes)"} ), True
        try:
            R = 6371.0
            phi1, phi2 = math.radians(ip["latitude"]),  math.radians(win["latitude"])
            dlat = math.radians(win["latitude"]  - ip["latitude"])
            dlon = math.radians(win["longitude"] - ip["longitude"])
            a = math.sin(dlat/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlon/2)**2
            dist = round(R * 2 * math.asin(math.sqrt(a)), 3)
            return str(
                {
                    "distance_km": dist,
                    "distance_note": (
                        "Écart faible" if dist < 5 else
                        "Écart modéré" if dist < 20 else
                        "Écart important"
                    ),
                    "win_accuracy_m": win.get("accuracy_m"),
                    "win_source":     win.get("position_source"),
                }
            ), True
        except Exception as exc:
            return str( {"note": f"Calcul impossible : {exc}"} ), True

    ip_data  = _get_ip()
    win_data = _get_windows()

    return str(
        {
            "generated_at":     datetime.datetime.utcnow().isoformat() + "Z",
            "ip_location":      ip_data,
            "windows_location": win_data,
            "comparison":       _compare(ip_data, win_data),
        }
    ), True

loadPrint()#c

logger = logging.getLogger(__name__)

loadPrint()#c

def _decode_header(value: str) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(str(part))
    return " ".join(result).strip()

loadPrint()#c

def _extract_body(msg: email.message.Message) -> dict:
    plain, html = [], []
    if msg.is_multipart():
        for part in msg.walk():
            if "attachment" in str(part.get("Content-Disposition", "")):
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            if part.get_content_type() == "text/plain":
                plain.append(text)
            elif part.get_content_type() == "text/html":
                html.append(text)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/html":
                html.append(text)
            else:
                plain.append(text)
    return {"plain": "\n".join(plain).strip(), "html": "\n".join(html).strip()}

loadPrint()#c

def _get_attachments(msg: email.message.Message) -> list:
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            if "attachment" in str(part.get("Content-Disposition", "")):
                attachments.append(_decode_header(part.get_filename() or "unknown"))
    return attachments

loadPrint()#c

def _connect(host: str, port: int, address: str, password: str) -> imaplib.IMAP4_SSL:
    """Open a fresh authenticated IMAP connection."""
    imap = imaplib.IMAP4_SSL(host, port)
    imap.login(address, password)
    return imap

loadPrint()#c

def _safe_logout(imap: imaplib.IMAP4_SSL) -> None:
    """Best-effort close/logout — never raises."""
    try:
        imap.close()
    except Exception:
        pass
    try:
        imap.logout()
    except Exception:
        pass

loadPrint()#c

def getEmail(
    address: str,
    password: str,
    folder: str = "INBOX",
    retries: int = 3,
    retry_delay: float = 2.0,
) -> list[dict]:
    """
    Retourne un array de dicts représentant chaque email non lu.

    Paramètres
    ----------
    address     : adresse email complète (ex: moi@gmail.com)
    password    : mot de passe d'application
    folder      : dossier IMAP à lire (INBOX par défaut)
    retries     : nombre de tentatives en cas d'erreur IMAP
    retry_delay : secondes d'attente entre chaque tentative

    Retour
    ------
    [
        {
            "id":           "42",
            "date":         "2024-03-15T10:30:00+00:00",
            "from":         "Alice <alice@example.com>",
            "to":           "Bob <bob@example.com>",
            "subject":      "Bonjour",
            "content-plain": "Contenu texte brut",
            "content-HTML":  "<p>Contenu HTML</p>",
            "attachments":  ["document.pdf"]
        },
        ...
    ]
    """
    domain = address.split("@")[-1].lower()
    host, port = IMAP_SERVERS.get(domain, (f"imap.{domain}", 993))

    last_exc: Exception | None = None

    for attempt in range(1, retries + 1):
        imap: imaplib.IMAP4_SSL | None = None
        try:
            imap = _connect(host, port, address, password)
            imap.select(folder)

            _, data = imap.search(None, "UNSEEN")
            ids = data[0].split()

            emails = []
            for uid in ids:
                _, raw = imap.fetch(uid, "(RFC822)")
                if not raw or raw[0] is None:
                    continue
                msg = email.message_from_bytes(raw[0][1])
                body = _extract_body(msg)

                date_str = msg.get("Date", "")
                try:
                    date = parsedate_to_datetime(date_str).isoformat()
                except Exception:
                    date = date_str

                emails.append({
                    "id":            uid.decode(),
                    "date":          date,
                    "from":          _decode_header(msg.get("From", "")),
                    "to":            _decode_header(msg.get("To", "")),
                    "subject":       _decode_header(msg.get("Subject", "")),
                    "content-plain": body["plain"],
                    "content-HTML":  body["html"],
                    "attachments":   _get_attachments(msg),
                })

            return emails  # success — exit immediately

        except (imaplib.IMAP4.abort, imaplib.IMAP4.error, OSError) as exc:
            last_exc = exc
            logger.warning("IMAP attempt %d/%d failed: %s", attempt, retries, exc)
            if imap is not None:
                _safe_logout(imap)
            if attempt < retries:
                time.sleep(retry_delay)

    return []
    # raise ConnectionError(
    #     f"IMAP connection failed after {retries} attempts: {last_exc}"
    # ) from last_exc

loadPrint()#c

# =====================
# TOOL: sendEmail
# =====================
def sendEmail( receiver: str, subject: str, text: str ):
    if receiver == "user-email":
        receiver = USER_EMAIL
    else:
        found = False
        for contact in CONTACT_LIST:
            if receiver == contact["name"]:
                receiver = contact["email"]
                found = True
                break
        if receiver.find( '@' ) != -1 and receiver.find( ".com" ) != -1:
            found = True
        if not found:
            return f"aucun contact trouvé pour {receiver}", True
    msg = MIMEText( text )
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver

    # print( f"{receiver=}, {subject=}, {text=}" )

    try:
        with smtplib.SMTP( SMTP_SERVER, SMTP_PORT ) as server:
            server.starttls()
            server.login( EMAIL, EMAIL_PASSWORD )
            server.sendmail( EMAIL, receiver, msg.as_string() )
        sendNotification( "Email envoyé", f"email envoyé à {receiver}" )
        log( "Email sent", "", 1 )
    except Exception as e:
        log( "Email error", str( e ), 3 )
        return "Envoie du courriel raté", True
    
    return "Envoie du courriel réussi", False

loadPrint()#c

# =====================
# TOOL: sleepSystem
# =====================
def sleepSystem( exception ):
    global conversation, called, AUDIO
    AUDIO = True
    GUI.setTextToDisplay( '' )
    GUI.textInput( False )
    GUI.displayRika( False )
    called = False
    # conversation.append(
    #     {
    #         "role": "system",
    #         "content": f"{moment()}"
    #     }
    # )
    if SERVER_URL:
        requests.post( f"{SERVER_URL}/{SET_CONVERSATION}", json=conversation )
    Json.write( conversation, "./conversation.json" )
    Sound.waitForVoiceToFinish()
    if exception:
        raise ExitAgent()
    # exit( 0 )

loadPrint()#c

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

loadPrint()#c

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

        content = [
            {
                "type": "text",
                "text": prompt
            }
        ]

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

    print( "ask model for vision" )
    response = Model.askModel( VISION_MODEL, messages, "high", MAX_RETRIES, Model.Verification.rawResponse )

    return f"voici l'image. Fait ce que {USERNAME} te demande de faire avec : " + response, True

loadPrint()#c

def removeEmojis( text ):
    emoji_pattern = re.compile(
        '['
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "\U00002B50-\U00002B55"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub( r'', text )

loadPrint()#c


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

def summarized( response: str ):
    if len( response.split( ' ' ) ) < 50:
        return response
    print( "ask model for summary" )
    summary = Model.askModel(
        ASK_MODEL,
        [
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
Raccourcis le message d'origine sans omettre d'informations importantes.
Le résultat doit OBLIGATOIREMENT avoir moins de 50 mots
Garde le plus d'informations importantes possible en respectant la limite de mots
""",
                "name": "instructions"
            },
            {
                "role": "user",
                "content": response
            }
        ],
        "none",
        MAX_RETRIES,
        Model.Verification.isJson
    )

    try:
        return json.loads( summary )["message"]
    except JSONDecodeError:
        return summary

loadPrint()#c

# def moment():
#     date = datetime.datetime.now()
#     day_name = int( date.strftime( "%w" ) )
#     if day_name == 0:
#         day_name = "Dimanche"
#     elif day_name == 1:
#         day_name = "Lundi"
#     elif day_name == 2:
#         day_name = "Mardi"
#     elif day_name == 3:
#         day_name = "Mercredi"
#     elif day_name == 4:
#         day_name = "Jeudi"
#     elif day_name == 5:
#         day_name = "Vendredi"
#     elif day_name == 6:
#         day_name = "Samedi"
#     jour = date.strftime( "%d" )
#     mois = int( date.strftime( "%m" ) )
#     if mois == 1:
#         mois = "Janvier"
#     elif mois == 2:
#         mois = "Février"
#     elif mois == 3:
#         mois = "Mars"
#     elif mois == 4:
#         mois = "Avril"
#     elif mois == 5:
#         mois = "Mai"
#     elif mois == 6:
#         mois = "Juin"
#     elif mois == 7:
#         mois = "Juillet"
#     elif mois == 8:
#         mois = "Août"
#     elif mois == 9:
#         mois = "Septembre"
#     elif mois == 10:
#         mois = "Octobre"
#     elif mois == 11:
#         mois = "Novembre"
#     elif mois == 12:
#         mois = "Décembre"
#     ans = date.strftime( "%Y" )
#     heure = datetime.datetime.now().strftime( "%H" )
#     minute = datetime.datetime.now().strftime( "%M" )
#     return str( f"{ans=} {mois=} {jour=} {heure=} {minute=}" )


loadPrint()#c

def treadTextResponse( response: str ):
    return response.replace( "**", '' )

loadPrint()#c

def treatAudioResponse( response ):

    # print( f"{AUDIO=}" )
    # print( "treatAudioResponse", response )

    say_response = response
    say_response = say_response.replace( '*', '' )
    say_response = removeEmojis( say_response )
    say_response = say_response.replace( '\n', '.' )


    say_response = say_response.split( "```" )
    code = 0
    for i in range( len( say_response ) ):
        if i % 2 == 1:
            extracted_code = say_response[i]

            extracted_code = extracted_code.split( "\n" )
            del extracted_code[0]
            extracted_code = "\n".join( extracted_code )

            planguage = extracted_code.split( '\n' )[0].replace( "```", '' )
            try:
                while os.path.exists( "./code/code-" + planguage + '-' + str( code ) + '.' + file_extensions[planguage.lower()] ):
                    code = random.randint( 1000, 9999 )
            except KeyError:
                while os.path.exists( "./code/code-" + planguage + '-' + str( code ) + ".txt" ):
                    code = random.randint( 1000, 9999 )

            say_response[i] = "extrait de code " + planguage + " numéro " + str( code ) + ", enregistré sur le pc"

    say_response = ' '.join( say_response )
    
    # for i in range( len( prononciation ) ):
    #     while say_response.find( list( prononciation.keys() )[i] ) != -1:
    #         say_response = say_response.replace( list( prononciation.keys() )[i], prononciation[list( prononciation.keys() )[i]] )
    
    # say_response = say_response.split( '`' )
    say_response = say_response.replace( '`', '' )

    Sound.waitForVoiceToFinish()
    Sound.generateVoice( say_response, VOICE )
    Sound.playVoice()

loadPrint()#c

def getUserInput():
    # print( "getting input" )
    user_input = ''
    if AUDIO:
        Sound.waitForVoiceToFinish()
        print( "YOU > ", end='' )
        user_input = Sound.listen()
        print( user_input )
    else:
        # user_input = input( "YOU > " )
        while True:
            print( GUI.getTextInputState() )
            if GUI.getTextInputState() == "hidden":
                break
            time.sleep( 1 )
        GUI.textInput( True )
        while True:
            time.sleep( 1 )
            user_input = GUI.getInput()
            if user_input:
                GUI.textInput( False )
                break
        # print( f"User input: {user_input}" )
    return user_input

loadPrint()#c

def treatResponse( response ):
    treated_text = treadTextResponse( response )
    print( f"{ASSISTANT_NAME} >", treated_text )
    GUI.setTextToDisplay( treated_text )
    if AUDIO:
        treatAudioResponse( response )

loadPrint()#c

# =====================
# MAIN LOOP
# =====================
def chat():
    global conversation, treating_response
    
    april_fools_rickroll()
    # print( "called" )

    # conversation.append(
    #     {
    #         "role": "system",
    #         "content": f"{moment()}"
    #     }
    # )

    while True:
        
        # print( "getting emails" )

        email_thread = ThreadWithReturnValue( target=getEmail, args=( EMAIL, EMAIL_PASSWORD ) )
        email_thread.start()
        
        # print( "asking user" )
        treating_response.join()
        user_input = getUserInput()
        
        emails = email_thread.join()
        for email in emails:
            conversation.append(
                {
                    "role": "user",
                    "content": "Email reçu :\n\n" + json.dumps( email, indent=4 ),
                    "name": "getEmail tool"
                }
            )

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
            print( "ask model for chatting (1)" )
            response = Model.askModel( MAIN_MODEL, conversation, "high", MAX_RETRIES, Model.Verification.isJson )

            content = json.loads( response )
            conversation.append( 
                {
                    "role": "assistant",
                    "content": response
                }
            )
            treating_response = threading.Thread( target=treatResponse, args=( content["message"], ) )
            treating_response.start()
            # treated_text = treadTextResponse( content["message"] )
            
            # print( f"{ASSISTANT_NAME} >", treated_text )
            # GUI.setTextToDisplay( treated_text )
            # if AUDIO:
            #     treatAudioResponse( content["message"] )
            
            not_understand = False
            do_response = False
            role = "assistant"
            last_do_response = do_response
            while len( content["tools"] ) != 0:
                for tool in content["tools"]:
                    print( f"{tool["name"]} tool" )
                    if tool["name"] == "analyseOldImage":
                        result, do_response = analyseImage( tool["params"]["source"], tool["params"]["prompt"], False )
                    elif tool["name"] == "analyseNewImage":
                        result, do_response = analyseImage( tool["params"]["source"], tool["params"]["prompt"], True )
                    elif tool["name"] == "sendEmail":
                        result, do_response = sendEmail( tool["params"]["receiver"], tool["params"]["subject"], tool["params"]["content"] )
                    elif tool["name"] == "openLink":
                        result, do_response = openLink( tool["params"]["query"] )
                    elif tool["name"] == "getLocalisation":
                        result, do_response = getLocalisation()
                    elif tool["name"] == "openApp":
                        result, do_response = openApp( tool["params"]["app"] )
                    elif tool["name"] == "doProtocol":
                        result, do_response = doProtocol( tool["params"]["protocol"] )
                    elif tool["name"] == "recognizeMusic":
                        result, do_response = recognizeMusic()
                    elif tool["name"] == "saveFile":
                        result, do_response = saveFile( tool["params"]["name"], tool["params"]["content"] )
                    elif tool["name"] == "webSearch":
                        result, do_response = webSearch( tool["params"]["query"] )
                    elif tool["name"] == "notUnderstand":
                        not_understand = True
                        break
                    elif tool["name"] == "sleepSystem":
                        sleepSystem( True )
                    else:
                        result = f"No tool found for {tool["name"]}"
                    
                    if not not_understand:

                        if type( result ) == str:
                            conversation.append( 
                                {
                                    "role": "user",
                                    "content": result,
                                    "name": f"{tool["name"]} tool"
                                }
                            )
                        else:
                            conversation.append( 
                                {
                                    "role": role,
                                    "content": result,
                                }
                            )
                    do_response = do_response or last_do_response
                    last_do_response = do_response
                if not_understand:
                    content["tools"] = []
                    break
                if do_response:
                    print( "ask model for chatting (2)" )
                    response = Model.askModel( MAIN_MODEL, conversation, "high", MAX_RETRIES, Model.Verification.isJson )
                    
                    conversation.append( 
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )
                    content = json.loads( response )
                    treating_response.join()
                    treating_response = threading.Thread( target=treatResponse, args=( content["message"], ) )
                    treating_response.start()
                    # treated_text = treadTextResponse( content["message"] )
                    # GUI.setTextToDisplay( treated_text )
                    # print( f"{ASSISTANT_NAME} >", treated_text )
                    # if AUDIO:
                    #     treatAudioResponse( content["message"] )
                else:
                    break

loadPrint()#c
time.sleep( 0.5 )

# =====================
# START
# =====================
try:
    if __name__ == "__main__":
        # print( "" )
        keyboard.add_hotkey( CALL_HOTKEY, toggleRika )
        check_audio_call.start()
        while True:
            # question = input( "...\n" )

            question = ""
            # if not AUDIO:
            #     question = "rika"
            #     # question = input( "...\n" )
            # else:
            # print( "..." )
            # question = Sound.listen()
            # print( question )
            # print( f"{called=}" )
            if called:
                try:
                    GUI.displayRika( True )
                    chat()
                except ExitAgent:
                    GUI.displayRika( False )
                    print( "Zzz..." )
            time.sleep( 2 )


except KeyboardInterrupt:

    GUI.quitGUI()
    Json.write( conversation, "./conversation.json" )
    # Sauvegarde brute pour debug
    for message in conversation:
        if message["role"] == "assistant":
            message["content"] = json.loads( message["content"] )
    Json.write( conversation, "./debug.json" )
    

    # Affichage formaté dans la console
    print( "\n📝 Debug conversation ( KeyboardInterrupt )\n" )
    for i, message in enumerate( conversation, start=1 ):
        role = message.get( "role", "unknown" )
        name = message.get( "name", '' )
        content = message.get( "content", '' )

        print( f"--- Message {i} ---" )
        if name:
            print( f"Name : {name}" )
        if isinstance( content, str ):
            print( f"Content : {content}" )
        else:
            # Si content est déjà un dict ou JSON
            print( f"Content : {json.dumps( content, ensure_ascii=False, indent=2 )}" )
        print( "--------------------\n" )