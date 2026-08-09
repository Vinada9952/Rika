print( "importing librairies..." )
from requests.exceptions import ConnectionError, Timeout, RequestException
from urllib.parse import unquote, urlparse, parse_qs
from pygrabber.dshow_graph import FilterGraph
from email.utils import parsedate_to_datetime
from spotipy.oauth2 import SpotifyOAuth
from email.header import decode_header
from email.mime.text import MIMEText
from json import JSONDecodeError
from groq import BadRequestError
from groq import APIStatusError
import speech_recognition as sr
from plyer import notification
from typing import List, Dict
from bs4 import BeautifulSoup
from shazamio import Shazam
from tkinter import font
import soundfile as sf
import win32clipboard
from PIL import Image
from groq import Groq
from ddgs import DDGS
import pyaudiowpatch
import tkinter as tk
import numpy as np
import webbrowser
import statistics
import subprocess
import threading
import tempfile
import requests
import edge_tts
import keyboard
import calendar
import datetime
import win32con
import win32api
import win32gui
import asyncio
import win32ui
import smtplib
import logging
import spotipy
import imaplib
import ctypes
import ollama
import base64
import pygame
import random
import socket
import email
import glob
import json
import math
import time
import cv2
import sys
import mss
import io
import re
import os

print( "Starting GUI..." )

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4, default=str )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

serveur_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

serveur_socket.bind( ( '0.0.0.0', Json.read( "./settings.json" )["gui"]["communication-port"] ) )
client_socket = None

socket_running = True
to_send = ""
queue_send = []

gui_mutex = threading.Lock()

def onReceiveSocket():
    global socket_running
    # Réception des données
    while socket_running:
        received = client_socket.recv( 1024 ).decode( 'utf-8' )
        if received.find( '\n' ) != -1:
            informations = received.split( '\n' )
        else:
            informations = [received]
        for i, information in enumerate( informations ):
            if len( information ) == 0:
                informations.pop( i )

        for information in informations:
            data = json.loads( information )
            if data["variable"] == "text_input_text":
                global text_input_text
                text_input_text = data["value"]
            elif data["variable"] == "text_input_state":
                global text_input_state
                text_input_state = data["value"]
            elif data["variable"] == "gui_ready":
                global gui_ready
                gui_ready = data["value"]
            # print( "new data receive in socket :", json.dumps( data, indent=4 ) )
        time.sleep( 0.1 )

def send():
    global to_send, queue_send, socket_running, client_socket, gui_mutex
    while socket_running:
        if queue_send:
            # Envoi d'un message au client
            message = None
            with gui_mutex:
                message = queue_send.pop( 0 )
            message = str( message )
            # message = message.replace( '\n', '' )
            if not message.endswith( "\n" ):
                message += "\n"
            client_socket.sendall( message.encode('utf-8') )
        else:
            time.sleep( 0.1 )

def sendDataSocket( value: str ):
    global queue_send, to_send, gui_mutex
    with gui_mutex:
        queue_send.append( value )

def quitSocket():
    global socket_running
    socket_running = False

socket_receive_thread = threading.Thread( target=onReceiveSocket, name="RIKA-RX-GUI" )
socket_send_thread = threading.Thread( target=send, name="RIKA-TX-GUI" )

socket_receive_thread.daemon = True
socket_send_thread.daemon = True

text_input_text = None
text_input_state = "hidden"

# def gui():
#     subprocess.run( ["python3", "./gui.py"] )
#     # os.system( "python3 ./gui.py" )

gui_ready = False

class GUI:
    def startGUI():
        global serveur_socket, client_socket, socket_send_thread, socket_receive_thread
        # thread_gui = threading.Thread( target=gui )
        # thread_gui.start()
        subprocess.Popen( ["python3", "./gui.py"], creationflags=subprocess.DETACHED_PROCESS, shell=False)
        serveur_socket.listen()
        client_socket, _ = serveur_socket.accept()
        socket_send_thread.start()
        socket_receive_thread.start()
        global gui_ready
        while not gui_ready:
            print( f"{gui_ready=}" )
            time.sleep( 1 )


    def quitGUI():
        global socket_send_thread, socket_receive_thread
        sendDataSocket(
            json.dumps(
                {
                    "function": "quitGUI",
                    "args": None
                }
            )
        )
        quitSocket()


    def setInit( state: bool ):
        sendDataSocket(
            json.dumps(
                {
                    "function": "setInit",
                    "args": (state)
                }
            )
        )

    def setLoading( load ):
        sendDataSocket(
            json.dumps(
                {
                    "function": "setLoading",
                    "args": (int( load ))
                }
            )
        )

    def displayRika( value ):
        sendDataSocket(
            json.dumps(
                {
                    "function": "displayRika",
                    "args": (value)
                }
            )
        )
    
    def setTextToDisplay( value ):
        sendDataSocket(
            json.dumps(
                {
                    "function": "setTextToDisplay",
                    "args": (value)
                }
            )
        )
    
    def textInput( value: bool ):
        sendDataSocket(
            json.dumps(
                {
                    "function": "textInput",
                    "args": (value)
                }
            )
        )

    def getInput():
        global text_input_text
        tmp = text_input_text
        text_input_text = None
        return tmp
    
    def getTextInputState():
        global text_input_state
        return text_input_state


GUI.startGUI()

print( "Starting Rika..." )

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
    def __init__(self, message = "Agent exit"):
        log( "ExitAgent", message, "error" )

loadPrint()#c

class NotValidResponse( Exception ):
    def __init__(self, message):
        log( "NotValidResponse", message, "error" )

loadPrint()#c

class NoResponseError( Exception ):
    def __init__(self, message):
        log( "NoResponseError", message, "error" )

loadPrint()#c

class FunctionEnd( SystemExit ):
    pass

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
sound_mutex = threading.Lock()
class Sound:
    def listenSRWhisper() -> str | int:
        def _recognize_fast(audio_data):
            r = sr.Recognizer()
            try:
                return r.recognize_google(audio_data, language="fr-FR")
            except:
                return ""

        def _recognize_whisper(audio_data, result_container):
            tmp_path = None

            try:
                wav_bytes = audio_data.get_wav_data()

                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    tmp.write(wav_bytes)
                    tmp_path = tmp.name

                for _ in range(MAX_RETRIES):
                    try:
                        with open(tmp_path, "rb") as f:
                            response = requests.post(
                                "http://localhost:20128/v1/audio/transcriptions",
                                headers={
                                    "Authorization": f"Bearer {OMNIROUTE_API_KEY}",
                                },
                                files={
                                    "file": ("audio.wav", f, "audio/wav")
                                },
                                data={
                                    "model": "auto",
                                    "language": "fr",
                                    "response_format": "text",
                                    "prompt": "Transcription de commandes vocales générales, langage naturel."
                                },
                                timeout=60
                            )

                        response.raise_for_status()

                        result_container["text"] = response.text.strip()
                        return

                    except Exception:
                        pass

                result_container["text"] = ""

            except Exception:
                result_container["text"] = ""

            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        def _fuse_with_llm(sr_text, whisper_text):
            # Cas critiques
            if not sr_text and not whisper_text:
                return -1
            if not sr_text:
                return whisper_text
            if not whisper_text:
                return sr_text

            # Skip si identique
            if sr_text == whisper_text:
                return sr_text

            config = """
Tu corriges une transcription vocale.

IMPORTANT :
- SR est souvent faux sur mots rares/tecnhiques
- Whisper hallucine souvent

Ta priorité ABSOLUE :
→ garder les mots rares de Whisper
→ garder la structure de SR

Règles STRICTES :
- N'invente RIEN
- Si un mot est différent entre les deux, choisis celui qui semble le plus adapté au contexte.
- Si aucun des 2 mots est adapté au contexte, choisis en un adapté au contexte (ex. Netherite et Minecraft)
- Si 2 mots peuvent être valide dans un même contexte, privilégie whisper
- Corrige les erreurs évidentes
- Phrase courte et naturelle
- Aucune explication

Exemples :
- SR: quelle est la meilleure couche dans Minecraft pour trouver de la NASA right
- WHISPER: Quelle est la meilleure couche en Minecraft pour trouver de la netherite ?
- result : Quelle est la meilleur couche dans Minecraft pour trouver le la netherite ?
        """

            prompt = f"""
SR:
{sr_text}

Whisper:
{whisper_text}

Phrase finale:
        """

            try:
                # response = Model.askGroqModel( SIMPLE_MODEL, [{"role": "system", "content": config}, {"role": "user", "content": prompt}], "low", MAX_RETRIES, Model.Verification.rawResponse )
                # response = Model.askModel(
                #     SIMPLE_MODEL,
                #     [
                #         {
                #             "role": "system",
                #             "content": config
                #         },
                #         {
                #             "role": "user",
                #             "content": prompt
                #         }
                #     ],
                #     verification=Model.Verification.rawResponse
                # )
                response = Model.askModel(
                    [
                        {
                            "role": "system",
                            "content": config
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    Model.Verification.rawResponse
                )
                return response
            except:
                return sr_text or whisper_text or -2

        r = sr.Recognizer()

        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise(source, duration=0.5)
            except:
                pass

            audio_data = r.listen(source, phrase_time_limit=6)

        # =========================
        # 1. SR EN PREMIER
        # =========================
        sr_text = _recognize_fast(audio_data)
        print( f"{sr_text=}" )

        if not sr_text:
            return -1

        # =========================
        # 2. WHISPER (SEULEMENT SI SR OK)
        # =========================
        whisper_result = {"text": ""}

        whisper_thread = threading.Thread(
            target=_recognize_whisper,
            args=(audio_data, whisper_result)
        )
        whisper_thread.start()

        # ⏱️ attendre un peu Whisper
        start_wait = time.time()
        while whisper_thread.is_alive():
            if time.time() - start_wait > 0.6:
                break
            time.sleep(0.01)

        whisper_text = whisper_result["text"]
        # if not whisper_text:
        #     return -1
        print( f"{whisper_text=}" )

        # =========================
        # 3. FUSION
        # =========================
        if not whisper_text:
            return sr_text

        return _fuse_with_llm(sr_text, whisper_text)

    def listen( language: str = "fr-FR" ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise( 1 )
            except AssertionError:
                pass
            # r.adjust_for_ambient_noise( 1 )
            audio_data = r.listen( source=source, phrase_time_limit=LISTEN_TIME_LIMIT )
        try:
            text = r.recognize_google( audio_data, language=language )
            text = str( text )
            return text
        except sr.UnknownValueError:
            return -1
    
    def getVoices():
        return edge_tts.list_voices()


    def _generateVoice( text, voice ):
        global sound_mutex
        is_correctly_generated = False
        while not is_correctly_generated:
            text = "   " + text.replace( '*', '' ).replace( '\n', ".     " )
            if type( voice ) == str:
                communicate = edge_tts.Communicate( text, voice )
                with sound_mutex:
                    communicate.save_sync( f"{CACHE_PATH}output.mp3" )
            else:
                communicate = edge_tts.Communicate( text, voice["ShortName"] )
                with sound_mutex:
                    communicate.save( f"{CACHE_PATH}output.mp3" )
            
            # Vérifier que le fichier a été créé et n'est pas vide
            if not os.path.exists( f"{CACHE_PATH}output.mp3" ) or os.path.getsize( f"{CACHE_PATH}output.mp3" ) == 0:
                pass
            else:
                is_correctly_generated = True
    
    def generateVoice( text, voice ):
        return Sound._generateVoice( text, voice )
    
    def _playVoice():
        global sound_mutex, VOICE_VOLUME
        try:
            with sound_mutex:
                pygame.mixer.music.load( f"{CACHE_PATH}output.mp3" )
                pygame.mixer.music.set_volume( VOICE_VOLUME )
            pygame.mixer.music.play()
        except pygame.error as e:
            log(
                "Failed to load MP3 file",
                {
                    "error": str( e ),
                    "file": f"{CACHE_PATH}output.mp3",
                    "file_exists": os.path.exists( f"{CACHE_PATH}output.mp3" ),
                    "file_size": os.path.getsize( f"{CACHE_PATH}output.mp3" ) if os.path.exists( f"{CACHE_PATH}output.mp3" ) else 0
                },
                "warning"
            )
            print( f"Erreur: Impossible de charger le fichier MP3: {e}" )
    
    def _playFile( file_path, reverse: bool = False ):
        global VOICE_VOLUME
        try:
            file_to_play = file_path
            
            if reverse:
                from pydub import AudioSegment
                import tempfile
                
                # Charger le fichier MP3
                audio = AudioSegment.from_mp3( file_path )
                # Inverser l'audio
                audio_reversed = audio.reverse()
                
                # Sauvegarder temporairement le fichier inversé
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    file_to_play = tmp.name
                audio_reversed.export( file_to_play, format="mp3" )
            
            pygame.mixer.music.load( file_to_play )
            pygame.mixer.music.set_volume( VOICE_VOLUME )
            pygame.mixer.music.play()
        except pygame.error as e:
            log(
                "Failed to load audio file",
                {
                    "error": str( e ),
                    "file": file_path,
                    "file_exists": os.path.exists( file_path ),
                    "file_size": os.path.getsize( file_path ) if os.path.exists( file_path ) else 0
                },
                "warning"
            )
            print( f"Erreur: Impossible de charger le fichier audio {file_path}: {e}" )
    
    def playVoice():
        return Sound._playVoice()
    
    def playFile( file_path, reverse: bool = False ):
        return Sound._playFile( file_path, reverse )
    
    def waitForSoundTofinish():
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick( 10 )
        pygame.mixer.music.unload()

loadPrint()#c

def hasWifiAccess( url = "http://www.google.com", timeout = 3 ) -> bool:
    """
    Tente d'établir une connexion avec un serveur externe fiable (Google)
    pour déterminer si un accès Internet est disponible.
    
    Retourne True si la connexion réussit, False sinon.
    """
    # URL de test : On utilise une URL très stable.
    # HEAD est utilisé car il ne télécharge que l'en-tête (plus rapide que GET).

    try:
        # On fait une requête HEAD au lieu de GET pour optimiser la bande passante
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        
        # Si la requête réussit (code de statut 200-399), l'Internet est fonctionnel.
        # On vérifie même si le code de statut est dans la plage "succès"
        if response.status_code < 400:
            # print("✅ Connexion réussie.")
            return True
        else:
            # print(f"❌ Échec de la connexion (Code {response.status_code}).")
            return False
             
    except ConnectionError:
        # Cette exception est levée si aucun réseau n'est détecté ou si le DNS échoue.
        # print("❌ Échec de la connexion réseau (Problème de câble, Wi-Fi, etc.).")
        return False
    except Timeout:
        # Cette exception est levée si le délai d'attente est dépassé.
        # print("⏳ Timeout de connexion (Le serveur ne répond pas à temps).")
        return False
    except RequestException as e:
        # Capture toutes les autres erreurs de la bibliothèque requests.
        # print(f"❌ Erreur réseau imprévue : {e}")
        return False

loadPrint()#c

log_mutex = threading.Lock()

loadPrint()#c

logs = []
def log( message, info, level ):
    global logs
    item = {
        "level": level,
        "message": message,
        "info": info,
        "moment": time.time()
    }
    with log_mutex:
        logs.append( item )
        tmp = logs.copy()
    tmp = sorted(tmp, key=lambda x: x['moment'])
    Json.write( tmp, f"{DEBUG_PATH}log.json" )

loadPrint()#c

class SpotifyPlayer:
    SCOPE = (
        "user-read-playback-state "
        "user-modify-playback-state "
        "user-read-currently-playing"
    )

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "https://127.0.0.1:9952/callback"):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=self.SCOPE,
            )
        )

    def openSpotify(self):
        """Lance Spotify sur l'ordinateur."""
        subprocess.Popen( ["C:\\Users\\Vincent Boucher\\AppData\\Roaming\\Spotify\\Spotify.exe"], creationflags=subprocess.DETACHED_PROCESS, shell=True)
        time.sleep( 5 )
        

    # ------------------------------------------------------------------ #
    #  Vérification des appareils                                          #
    # ------------------------------------------------------------------ #

    def _get_active_device(self) -> str | None:
        """Retourne l'ID du premier appareil actif, ou None si aucun."""
        devices = self.sp.devices().get("devices", [])
        for d in devices:
            if d["is_active"]:
                return d["id"]
        return None

    def _ensure_device(self) -> str | None:
        """
        Vérifie qu'un appareil Spotify est disponible.
        Si aucun n'est trouvé, appelle openSpotify() et réessaie.
        Retourne l'ID de l'appareil, ou None si toujours indisponible.
        """
        devices = self.sp.devices().get("devices", [])

        if not devices:
            # print("⚠️  Aucun appareil Spotify détecté. Lancement de Spotify...")
            self.openSpotify()

            # Réessaie jusqu'à 5 fois avec 1 seconde d'intervalle
            for attempt in range(5):
                time.sleep(1)
                devices = self.sp.devices().get("devices", [])
                if devices:
                    # print("✅  Spotify détecté !")
                    break
            else:
                # print("❌  Spotify n'a pas pu être lancé.")
                return None

        # Retourne l'appareil actif, sinon le premier disponible
        for d in devices:
            if d["is_active"]:
                return d["id"]
        return devices[0]["id"]

    # ------------------------------------------------------------------ #
    #  Lecture / Pause / Stop                                              #
    # ------------------------------------------------------------------ #
    def setVolume(self, volume: int, device):
        """Définit le volume (0-100)."""
        
        # Limiter le volume entre 0 et 100
        volume = max(0, min(100, volume))
        self.sp.volume(volume, device)
        # print(f"🔊  Volume : {volume}%")

    def play(self, uri: str | None = None, device_id: str | None = None):
        if device_id is None:
            device_id = self._ensure_device()
            if device_id is None:
                return  # Abandon si Spotify n'est pas disponible

        kwargs = {"device_id": device_id}
        if uri:
            if uri.startswith("spotify:track:"):
                kwargs["uris"] = [uri]
            else:
                kwargs["context_uri"] = uri
        self.sp.start_playback(**kwargs)
        # print(f"▶  Lecture lancée{' : ' + uri if uri else ''}")

    def pause(self):
        self.sp.pause_playback()
        # print("⏸  Pause")

    def resume(self):
        self.sp.start_playback()
        # print("▶  Reprise")

    def nextTrack(self):
        self.sp.next_track()
        # print("⏭  Titre suivant")

    def previousTrack(self):
        self.sp.previous_track()
        # print("⏮  Titre précédent")

    def shuffle(self, state: bool = True):
        self.sp.shuffle(state)
        # print(f"🔀  Shuffle : {'activé' if state else 'désactivé'}")

    def nowPlaying(self) -> dict | None:
        time.sleep( 0.5 )
        current = self.sp.current_playback()
        if not current or not current.get("item"):
            return None
        track = current["item"]
        Json.write( track, "a.json" )
        if current["is_playing"]:
            info = {
                "name": track["name"],
                "artists": ", ".join(a["name"] for a in track["artists"]),
                "album": track["album"]["name"],
                "publication": ""
            }
            return info
        return None

    def listDevices(self) -> list[dict]:
        devices = self.sp.devices().get("devices", [])
        return devices

    def search(self, query: str, search_type: str = "track", limit: int = 5) -> list[dict]:
        results = self.sp.search(q=query, type=search_type, limit=limit)
        
        types = search_type.split(",")
        items = []
        
        for t in types:
            key = f"{t.strip()}s"  # "track" -> "tracks", "playlist" -> "playlists"
            if key in results:
                for item in results[key]["items"]:
                    if item is not None:  # ← filtre les None
                        item["_search_type"] = t.strip()  # on tag chaque item avec son type
                        items.append(item)
        
        return items, search_type

    class SearchTypes:
        def mix( *types ):
            return ','.join( types )

        TRACK = "track"
        ALBUM = "album"
        ARTIST = "artist"
        PLAYLIST = "playlist"

        def isInTypes( types ):
            if type( types ) == str:
                if types.find( ',' ) != -1:
                    types = types.split( ',' )
                else:
                    if types not in ["track", "album", "artist", "playlist"]:
                        return False
            if type( types ) == list:
                for item in types:
                    if item not in ["track", "album", "artist", "playlist"]:
                        return False
            return True

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

def getAllApps() -> list[dict]:
    """
    Retourne la liste de toutes les applications installées sur l'ordinateur.
    Compatible Windows, macOS et Linux.

    Returns:
        list[dict]: Liste de dicts avec les clés 'name' et 'path'.
    """
    platform = sys.platform

    return _get_apps_windows()

loadPrint()#c

def omnirouteServer():
    os.system( "omniroute" )
    # subprocess.Popen( ["omniroute"], creationflags=subprocess.DETACHED_PROCESS, shell=False)

loadPrint()#c

# =====================
# CONFIG
# =====================

settings = Json.read( "settings.json" )

loadPrint()#c

OMNIROUTE_API_KEY = settings["api"]["api-key"]

loadPrint()#c

# ollama client
ollama_client = ollama.Client()

loadPrint()#c

# call settings
call_names = settings["call"]["names"]
call_names = sorted( call_names, key=len, reverse=True )
# print( call_names )
CALL_HOTKEY = settings["call"]["hotkey"]

loadPrint()#c

# models settings
MAX_RETRIES = settings["api"]["max-api-retries"]
ASSISTANT_NAME = settings["assistant-name"]

loadPrint()#c

# Audio settings
AUDIO = settings["audio"]["audio"]
VOICE = settings["audio"]["voice"]
AUDIO_DURATION_LIMIT = settings["audio"]["audio-duration-threshold"]
CONFIRMATION_SOUND = settings["audio"]["confirmation-sound"]
LISTEN_TIME_LIMIT = settings["audio"]["listen-time-limit"]
VOICE_VOLUME = settings["audio"]["voice-volume"]

loadPrint()#c

# Vision settings
SCREENSHOT_DIR = settings["directories"]["cache"]["screenshots"]
WEBCAM_PATH = settings["directories"]["cache"]["webcam"]

loadPrint()#c

# code file creation settings
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

# Music recognition settings
SAMPLE_RATE = 44100
DURATION = 8
TIMEOUT = 12
SPEAKER_SILENCE_THRESH = 0.005
MIC_SILENCE_THRESH = 0.0005 # beaucoup plus sensible que le speaker
MIC_GAIN = 5.0 # multiplie le volume du micro (augmente si encore trop faible)

loadPrint()#c

# Email settings
SMTP_SERVER = settings["email"]["smtp"]["server"]
SMTP_PORT = settings["email"]["smtp"]["port"]
EMAIL = settings["email"]["agent-email"]["email"]
EMAIL_PASSWORD = settings["email"]["agent-email"]["pwd"]
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

# directories settings
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

CACHE_PATH = settings["directories"]["cache"]["cache"]
DEBUG_PATH = settings["directories"]["debug"]


loadPrint()#c

for element in os.listdir( CACHE_PATH ):
    chemin = os.path.join( CACHE_PATH, element )
    if os.path.isfile( chemin ):
        os.remove( chemin )
        # print( f"Supprimé : {chemin}" )

loadPrint()#c

# User info settings
USERNAME = settings["email"]["user-email"]["name"]
USER_EMAIL = settings["email"]["user-email"]["email"]
PASSWORD = settings["email"]["user-email"]["pwd"]
CONTACT_LIST = Json.read( settings["directories"]["assets"]["contacts"] )
USERNOTE_DIRECTORY = settings["directories"]["assets"]["usernote"]

names = []
for contact in CONTACT_LIST:
    name = contact["name"]
    relation = contact["relation"]
    language = contact["language"]
    names.append( f"    -> {name} ({relation}) - Langue parlé : {language}" )

CONTACT_NAMES = '\n'.join( names )

loadPrint()#c

# Wifi settings
WIFI = hasWifiAccess()
# print( f"{WIFI=}" )
log( "Wifi connexion", WIFI, "info" )

loadPrint()#c

os.makedirs( "./cache", exist_ok=True )
os.makedirs( "./cache/screenshots", exist_ok=True )

loadPrint()#c

# Spotify settings
SPOTIFY_CLIENT_ID = settings["spotify-player"]["client-id"]
SPOTIFY_CLIENT_SECRET = settings["spotify-player"]["client-secret"]

if WIFI:
    try:
        spotify = SpotifyPlayer( SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET )
        IS_THERE_SPOTIFY = True
    except Exception as e:
        IS_THERE_SPOTIFY = False
        log( "Error creating spotify instance", str( e ), "warning" )
else:
    IS_THERE_SPOTIFY = False
    log( "No wifi access", "Spotify features will be unavailable", "warning" )
DEFAULT_VOLUME = settings["spotify-player"]["default-spotify-volume"]

formatted_devices = ""
DEVICES = settings["spotify-player"]["available-devices"]
DEFAULT_DEVICE = settings["spotify-player"]["default-device"]
for device in DEVICES:
    formatted_devices += f"\n    -> {device}"


PLAYLISTS = Json.read( settings["directories"]["assets"]["playlists"] )
playlists_formatted = ''
for playlist in PLAYLISTS:
    playlists_formatted += f"\n    -> {playlist["name"]} ({playlist["type"]}): {playlist["description"]}"

loadPrint()#c

NOTIFICATIONS = settings["gui"]["notifications"]

loadPrint()#c

THEME_COLOR = settings["gui"]["color"]

loadPrint()#c

# server settings
SERVER_URL = settings["server"]["url"]
SET_CONVERSATION = settings["server"]["set-conversation"]
GET_CONVERSATION = settings["server"]["get-conversation"]

loadPrint()#c

# Custom protocols settings
PROTOCOLS = [ { "name": settings["reset-protocol-name"], "command": "/delete-memory", "description": "" } ] + Json.read( settings["directories"]["assets"]["protocols"] )

protocol_list = ''
for protocol in PROTOCOLS:
    if protocol["description"]:
        protocol_list += f"\n    -> {protocol["name"]} ({protocol["command"]}): {protocol["description"]}"
    else:
        protocol_list += f"\n    -> {protocol["name"]}"

loadPrint()#c

# apps settings
def getAllAppsThread():
    global APPLICATIONS
    APPLICATIONS = getAllApps()
    Json.write( APPLICATIONS, f"{CACHE_PATH}applications.json" )
    APPLICATIONS = None
    sendNotification( "Scan des applications installés terminées" )

get_all_apps_thread = threading.Thread( target=getAllAppsThread, name="scanapps" )
get_all_apps_thread.start()

loadPrint()#c

# temporary variable(s)
treating_response = Substitute()

loadPrint()#c

CONVERSATION_PATH = settings["directories"]["assets"]["conversation"]

loadPrint()#c

# Conversation settings
# conversation = Json.read( CONVERSATION_PATH )
# if SERVER_URL:
#     data = requests.get( f"{SERVER_URL}/{GET_CONVERSATION}" )
#     conversation = data.json()
#     del data

conversation_mutex = threading.Lock()
# data = Json.read( "./conversation.json" )
# print( data )
# print( data.json() )
# conversation = data.json()["conversation"]
# print( conversation  )

loadPrint()#c

# TOOLS = [
#     {
#         "type": "function",
#         "function": {
#             "name": "getTime",
#             "description": "Retourne la date et l'heure courante du système.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "getLocalisation",
#             "description": "Retourne la localisation de l'utilisateur.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "getWeather",
#             "description": "Retourne la météo de la localisation actuelle de l'utilisateur.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "startChrono",
#             "description": "Partir un chronomètre.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "stopChrono",
#             "description": "Arrêter le chronomètre et retourner le temps mesuré.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "startTimer",
#             "description": "Partir un timer.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "duration": {
#                         "type": "integer",
#                         "description": "Temps du timer, en secondes."
#                     },
#                     "message": {
#                         "type": "string",
#                         "description": "Message à dire à la fin du timer."
#                     }
#                 },
#                 "required": ["duration", "message"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "getRemainingTime",
#             "description": "Retourne le temps restant du timer en cours.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "sleepSystem",
#             "description": "Met l'assistant en veille lorsque l'utilisateur n'a plus besoin de lui.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "analyseNewImage",
#             "description": "Analyse une nouvelle image depuis une capture d'écran ou une webcam.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "source": {
#                         "type": "string",
#                         "enum": ["screenshot", "webcam"]
#                     },
#                     "prompt": {
#                         "type": "string",
#                         "description": "Ce que tu veux savoir de l'image."
#                     }
#                 },
#                 "required": ["source", "prompt"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "analyseOldImage",
#             "description": "Analyse une image précédemment capturée dans la conversation.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "source": {
#                         "type": "string",
#                         "enum": ["screenshot", "webcam"]
#                     },
#                     "prompt": {
#                         "type": "string",
#                         "description": "Ce que tu veux savoir de l'image."
#                     }
#                 },
#                 "required": ["source", "prompt"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "openApp",
#             "description": "Ouvre une application installée sur l'ordinateur.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "app": {
#                         "type": "string",
#                         "description": "Nom de l'application à ouvrir."
#                     }
#                 },
#                 "required": ["app"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "openLink",
#             "description": "Ouvre un lien internet ou effectue une recherche web.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "Description ou lien à ouvrir."
#                     },
#                     "link": {
#                         "type": "string",
#                         "description": "Lien direct à ouvrir si nécessaire."
#                     }
#                 },
#                 "required": ["query"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "sendEmail",
#             "description": "Envoie un courriel à un destinataire. Liste de contacts disponible : " + CONTACT_NAMES,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "receiver": {
#                         "type": "string",
#                         "description": "Destinataire de l'email.",
#                         "enum": [contact["name"] for contact in CONTACT_LIST]
#                     },
#                     "subject": {
#                         "type": "string",
#                         "description": "Sujet de l'email."
#                     },
#                     "content": {
#                         "type": "string",
#                         "description": "Contenu de l'email."
#                     }
#                 },
#                 "required": ["receiver", "subject", "content"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "doProtocol",
#             "description": "Exécute un protocole prévu par le système. Liste des protocoles disponibles : " + protocol_list,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "protocol": {
#                         "type": "string",
#                         "description": "Nom du protocole à utiliser.",
#                         "enum": [protocol["name"] for protocol in PROTOCOLS]
#                     }
#                 },
#                 "required": ["protocol"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "saveFile",
#             "description": "Sauvegarde un fichier texte ou un script.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "name": {
#                         "type": "string",
#                         "description": "Nom du fichier à créer."
#                     },
#                     "content": {
#                         "type": "string",
#                         "description": "Contenu du fichier."
#                     }
#                 },
#                 "required": ["name", "content"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "webSearch",
#             "description": "Effectue une recherche sur le web.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "Terme ou question à rechercher."
#                     }
#                 },
#                 "required": ["query"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "playMusic",
#             "description": "Joue de la musique sur Spotify. Liste des appareils disponibles : " + formatted_devices + ". Liste des playlists disponibles : " + playlists_formatted + "Volume par défaut : " + str( DEFAULT_VOLUME ) + "%",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "search": {
#                         "type": "string",
#                         "description": "Recherche à effectuer sur Spotify."
#                     },
#                     "type": {
#                         "type": "string",
#                         "description": "Type de contenu: track, album, artist ou playlist.",
#                         "enum": ["track", "album", "artist", "playlist"]
#                     },
#                     "device": {
#                         "type": "string",
#                         "description": "Appareil sur lequel jouer la musique.",
#                         "enum": DEVICES
#                     },
#                     "volume": {
#                         "type": "integer",
#                         "description": "Volume de lecture."
#                     }
#                 },
#                 "required": ["search", "type", "device", "volume"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "setMusicState",
#             "description": "Met la lecture de musique en pause ou reprend la lecture.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "state": {
#                         "type": "boolean",
#                         "description": "false pour mettre en pause, true pour reprendre."
#                     }
#                 },
#                 "required": ["state"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "changeMusicTrack",
#             "description": "Change la piste Spotify en cours.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "target": {
#                         "type": "string",
#                         "description": "next ou previous.",
#                         "enum": ["next", "previous"]
#                     }
#                 },
#                 "required": ["target"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "recognizeMusic",
#             "description": "Reconnaît la musique qui joue.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "setIncognito",
#             "description": "Active ou désactive le mode incognito.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "value": {
#                         "type": "boolean",
#                         "description": "true pour activer, false pour désactiver."
#                     }
#                 },
#                 "required": ["value"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "getIncognito",
#             "description": "Retourne l'état actuel du mode incognito.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "createChart",
#             "description": "Crée un diagramme graphique à partir de données. Utilise cet outil pour répondre avec un graphique quand il y a des données, au lieu de les afficher directement. Exemples de format JSON : bandChart et lineChart utilisent un objet clef-valeur, pieChart utilise un objet de proportions, boxChart utilise un objet de listes de valeurs.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "type": {
#                         "type": "string",
#                         "description": "Type de diagramme: bandChart, pieChart, lineChart ou boxChart.",
#                         "enum": ["barChart", "pieChart", "lineChart", "boxChart"]
#                     },
#                     "title": {
#                         "type": "string",
#                         "description": "Titre du diagramme."
#                     },
#                     "x_axis_title": {
#                         "type": "string",
#                         "description": "Titre de l'axe X du diagramme, si présent. Met le vide si pas nécessaire. Mets les unités de mesure s'il y en a."
#                     },
#                     "y_axis_title": {
#                         "type": "string",
#                         "description": "Titre de l'axe Y du diagramme, si présent. Met le vide si pas nécessaire. Mets les unités de mesure s'il y en a."
#                     },
#                     "data": {
#                         "type": "object",
#                         "description": "Données pour le diagramme. Le format dépend du type de diagramme :\n- bandChart : {\"A\": 10, \"B\": 20}\n- pieChart : {\"Partie 1\": 30, \"Partie 2\": 70}\n- lineChart : {\"Jour 1\": 5, \"Jour 2\": 15}\n- boxChart : {\"Groupe 1\": [1, 2, 3, 4], \"Groupe 2\": [2, 3, 5, 6]}.",
#                     }
#                 },
#                 "required": ["type", "title", "x_axis_title", "y_axis_title", "data"],
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "createWidget",
#             "description": "Crée un widget affichable dans l'interface.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "description": {
#                         "type": "string",
#                         "description": "Description du widget à créer."
#                     }
#                 },
#                 "required": ["description"],
#             }
#         }
#     }
# ]

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

- getTime
  - Obtenir l'heure, la date, etc.

- getLocalisation
  - Obtenir la localisation de l'utilisateur
  - exemples de cas d'utilisation:
    -> Où suis-je ?

- getWeather
  - Obtenir la météo de la localisation actuelle de l'utilisateur

- startChrono
  - partir un chronomètre.
  - Tu peux en partir uniquement un à la fois.

- stopChrono
  - arrêter le chronomètre et retourner le temps mesuré

- startTimer
  - partir un timer
  - un seul timer à la fois
  - params:
    -> duration (float) : temps du timer, en secondes
    -> message (string) : message à dire à la fin du timer

- getRemainingTime
  - obtenir le temps restant du timer

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

- analyseNewImage
  - UTILISATION OBLIGATOIRE si l'utilisateur demande de REGARDER, VOIR, MONTRER, OBSERVER ou si aucune image n'a encore été analysée dans la conversation.
  - Si tu ne comprends pas la demande de l'utilisateur car il n'y a pas de contexte pour la réponse, utilise cet outil pour voir s'il y a une question ou une demande à l'écran.
  - Réutilise l'outil chaque fois que l'utilisateur ne donne pas de contexte, question, etc.
  - Cette action capture TOUJOURS une NOUVELLE image avant analyse.
  - params:
    -> source (string): "screenshot"|"webcam"
    -> prompt (string): ce que tu veux savoir de l'image
  - À utiliser pour:
    -> Regarde
    -> Que vois-tu ?
    -> Regarde mon écran
    -> Regarde la webcam
    -> J'ai un bug (sans analyse précédente)
    -> Observe

- analyseOldImage
  - UTILISATION OBLIGATOIRE uniquement si une image a DÉJÀ été capturée dans la conversation ET que l'utilisateur demande une analyse supplémentaire ou une précision.
  - À utiliser uniquement si l'utilisateur demande une clarification, sinon utiliser analyseNewImage
  - params:
    -> source (string): "screenshot"|"webcam"
    -> prompt (string): ce que tu veux savoir de l'image
  - À utiliser pour:
    -> Regarde mieux
    -> Analyse plus en détail
    -> Que vois-tu d'autre ?
    -> Zoom sur...
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
  - Quand tu écris à quelqu'un, écrit-lui toujours dans la langue que la personne parle. Adapte la langue du courriel en fonction, donc Français, Anglais, Suédois, Vietnamien, etc.

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

- playMusic
  - Faire jouer quelque chose sur spotify. Quand l'utilisateur te demande de faire jouer de la musique, l'ajouter sur spotify ou de chanter, utilise cet outil.
  - params:
    -> search (string): Ce que tu cherches sur spotify. Le plus précis possible.
    -> type (string): Le type du contenu recherché.
    -> device (string) : L'appareil sur lequel jouer la musique
    -> volume (int) : niveau de volume
  - types possibles:
    -> track
    -> album
    -> artist
    -> playlist
  - Différentes playlist de l'utilisateur:{playlists_formatted}
  - Liste d'appareils disponibles:{formatted_devices}
  - l'appareil par défaut est "{DEFAULT_DEVICE}". Si l'utilisateur ne demande pas d'appareils précis, utilise celui-ci
  - Le volume par défaut est {DEFAULT_VOLUME}. Si l'utilisateur ne demande pas un volume précis, utilise celui-ci

- setMusicState
  - Pauser/reprendre la musique
  - params:
    -> state (bool): false pour mettre la musique sur pause ou l'arrêter, true pour la reprendre ou la partir

- changeMusicTrack
  - Changer la musique qui joue
  - params:
    -> target (string): la musique à jouer
  - target doit soit être "next" OU "previous"

- recognizeMusic
  - Reconaitre la musique qui joue

- setIncognito
  - Mode de navigation privé. Si à true, active le mode de navigation privé. Le désactive à false
  - params:
    -> value (bool): si activé ou non

- getIncognito
  - Savoir si le mode incognito est activé (alias navigation privé)

- createChart
  - créer un diagramme
  - exemples d'utilisation:
    -> quelle est la production de prétrole des 10 dernières années
    -> Combien de médailles olympiques ont chaque pays d'Europe gagnés
  - params:
    -> type (string): Le type de diagramme que tu veux créer
    -> title (string): Le titre du diagramme
    -> x-axis-title (string): Le titre de l'axe X du diagramme, si présent. Met le vide si pas nécéssaires. Met les unitées de mesures s'il y en a
    -> y-axis-title (string): Le titre de l'axe y du diagramme, si présent. Met le vide si pas nécéssaires. Met les unitées de mesures s'il y en a
    -> data (json): Les données pour le diagramme. En fonction du diagramme, le format peut être différent
  - types et formats:
    -> bandChart:
      - diagramme à bande
      - à utiliser par défaut
      - format:
        {"{"}
          "colone sur l'axe X 1 (string)": donnée axe y 1 (float),
          "colone sur l'axe X 2 (string)": donnée axe y 2 (float),
          "colone sur l'axe X 3 (string)": donnée axe y 3 (float)
        {"}"}
    -> pieChart:
      - diagramme à pointes de tarte
      - À utiliser pour démontrer une proportion
      - Les valeurs n'ont pas besoind d'être sur 100, 360 ou 2pi, donne les vrais valeurs, la fonction va s'en occuper toute seule pour définir les proportion
      - format:
        {"{"}
          "nom de la région 1 (string)": valeur de la région 1 (float),
          "nom de la région 2 (string)": valeur de la région 2 (float),
          "nom de la région 3 (string)": valeur de la région 3 (float)
        {"}"}
    -> lineChart:
      - diagramme à lignes brisées
      - À utiliser pour démontrer une donnée au travers du temps, d'événements ou d'un parcours
      - format:
        {"{"}
          "point sur l'axe X 1 (string)": donnée axe y 1 (float),
          "point sur l'axe X 2 (string)": donnée axe y 2 (float),
          "point sur l'axe X 3 (string)": donnée axe y 3 (float)
        {"}"}
    -> boxChart:
      - diagramme de quartiles
      - À utiliser pour démontrer un étendu, une dispersion et/ou une concentration
      - format:
        {"{"}
          "groupe 1 (string)": [donnée1-1, donnée1-2, donnée1-3, donnée1-4],
          "groupe 2 (string)": [donnée2-1, donnée2-2, donnée2-3, donnée2-4],
          "groupe 3 (string)": [donnée3-1, donnée3-2, donnée3-3, donnée3-4]
        {"}"}

- createWidget
  - Créer un widget
  - params:
    -> description (string): une description du widget. Le plus précis possible
  - À utiliser quand l'utilisateur te demande d'afficher quelque chose
  - exemples d'utilisation:
    -> Affiche moi la batterie
    -> Affiche moi la météo
  - Donne le plus d'informations possibles
  - Exemples:
    -> utilisateur: affiche moi la météo → description: widget météo pour (localisation, à chercher avec getLocalisation)
    -> utilisateur: quelles sont les performances de l'ordi → description: utilisation RAM, GPU, CPU, SSD, réseau
  - Met un widget pour chaque éléments différents. Par exemple si l'utilisateur te demande la météo et les performances dans un même prompt, fait 2 widgets

RÈGLES IMPORTANTES :
- Soit consis, exact, juste, précis
- Ne JAMAIS écrire autre chose que du JSON.
- L'ordre d'apparition des outils dans "tools": [] est l'ordre d'exécution des outils
- Si aucune action n'est nécessaire, tools DOIT être [].
- Si une action est demandée, "tools" ne doit JAMAIS être vide.
- Si l'utilisateur demande un lien, **NE DONNE PAS LE LIEN DANS LE MESSAGE**, mets toujours un tool openLink.
- Quand on te demande d'ouvrir quelque chose, vérifie si c'est une application ou un lien, et ouvrir le bon outil en question
- Quand on te demande de voir ou de regarder, c'est avec l'outil d'analyse d'image (ancienne ou nouvelle, dépendament du contexte).
- Si tu hésites entre analyseNewImage et analyseOldImage, utilise toujours analyseNewImage.
- Quand l'utilisateur te demande explicitement de répondre ou une réponse et que tu ne comprends pas ou qu'il n'y a pas de contexte/réponse, regarde à l'écran avec l'outil analyseNewImage pour voir s'il y a une question à l'écran.
- Quand tu utilise un outil, donne toujours tout les paramètres et arguments nécéssaires.
- À CHAQUE FOIS que l'utilisateur demande d'envoyer un couriel, tu dois OBLIGATOIREMENT utiliser l'outil sendEmail.
- En envoyant des email, ne te fait pas passer pour l'utilisateur, mais pour son assistant. 
- Dans les email, ne parle pas de l'utilisateur à la 1re personne, mais à la 3e personne.
- Quand tu répond que tu as envoyé un email, FAIT-LE avec l'outil sendEmail
- Chaque fois qu'on te demande la météo, date ou localisation, ne te fie pas sur l'historique de la conversation, mais va chercher à chaque fois les outils
- À la fin de chaque email, signe ton nom et met une formule de politesse
- Dans les email, met le courriel dans la langue parlé du destinataire
- Si l'utilisateur te demande de faire quelque chose que tu n'es pas capable de faire, va voir dans les protocols
- Ne dis JAMAIS les paramètres utilisés pour les outils.
- utilise l'outil createChart dès que tu as des donnée à dire au lieu de les afficher
- ne dit JAMAIS des données demandés dans la clé "message", mais utilise l'outil createChart
- NE DONNE JAMAIS DE CODE DANS LA CLÉ "message", utilise toujours l'outil saveFile
- Ne fait JAMAIS de résumé de conversation, sauf quand je te le demande.
- Si une action est requise (ex: envoyer un email, ouvrir une app, ouvrir un lien, analyser une image), la réponse est invalide si aucun outil n'est appelé.
- Dès que tu reçois un email, dit le à l'utilisateur et un résumé de son contenu, et fait le pour chaque email. Si l'utilisateur n'a pas reçu d'email, n'en parle pas
- Il est INTERDIT de simuler une action dans le message sans appeler l'outil correspondant.
- Si une action est nécéssaire, ne te contente pas juste de répondre, FAIT l'action
- Ne met pas de mise en page ou des choses dans le genre pour faire des tableaux, titres en gras, ressort un texte simple destiné à être affiché dans le terminal
- Essaie de faire les messages les plus courts possibles
- Ta réponse est fait pour être dite à l'oral. Garde des caractères normaux pouvant être dit par un module TTS. C'est à dire, ne met pas de parenthèses et autres trucs du genre
"""

loadPrint()#c

# =====================
# SETUP
# =====================
for file in os.listdir( SCREENSHOT_DIR ):
    os.remove( os.path.join( SCREENSHOT_DIR, file ) )
os.makedirs( SCREENSHOT_DIR, exist_ok=True )

loadPrint()#c

def getCameraIndex( search ):
    return 0 # FIXME

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

fast_called = False
prompt = ""

loadPrint()#c

poncuation = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''

loadPrint()#c

def checkAudioCall():
    global called, fast_called, prompt
    while True:
        # print( f"check if called by audio : {called=}" )
        if not called:
            print( "..." )
            # question = Sound.listen()
            question = Sound.listenSRWhisper()

            if type( question ) == str:
                formatted = question.translate( str.maketrans( '', '', poncuation ) )
                calls = formatted.lower().split( ' ' )
                for call_name in call_names:
                    for call in calls:
                        if call.lower() == call_name.lower():
                            log(
                                "call name found",
                                json.dumps(
                                    {
                                        "full": question,
                                        "detected": call_name,
                                        "all": call_names,
                                        "agent": ASSISTANT_NAME
                                    },
                                    indent=4
                                ),
                                "info"
                            )
                            prompt = question.lower().replace( call_name.lower(), ASSISTANT_NAME )
                            if len( calls ) > 1:
                                fast_called = True
                                print( prompt )
                            called = True
                            break
                    if called:
                        break
            if not called:
                print( question )
            if called and not fast_called:
                print( ASSISTANT_NAME )
        else:
            time.sleep( 1 )

check_audio_call = threading.Thread( target=checkAudioCall, name="Check voice call" )

loadPrint()#c

def sendNotification( message ):
    if NOTIFICATIONS:
        notification.notify(
            title=ASSISTANT_NAME,
            message=message,
            app_name=ASSISTANT_NAME,
            timeout=3
        )

loadPrint()#c


class Model:
    def askModel( conversation, verification ):
        # if WIFI:
        for i in range( MAX_RETRIES ):
            response = requests.post(
                "http://localhost:20128/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OMNIROUTE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "auto",
                    "messages": conversation,
                    "stream": False
                }
            )

            response.raise_for_status()

            if verification( response.json()["choices"][0]["message"]["content"] ):
                break
        
        return response.json()["choices"][0]["message"]["content"]

    def askVisionModel(image: str, prompt: str, model: str = "qwen3.6") -> str:

        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image]
                    }
                ]
            )

            return response["message"]["content"]
        except Exception as e:
            log(
                "askVisionModel error",
                json.dumps(
                    {
                        "error": str(e),
                        "prompt": prompt,
                        "model": model
                    },
                    indent=4
                ),
                "error"
            )
            return "Erreur lors de l'analyse de l'image."


    def askWebModel(query: str, max_pages: int = 5):
        """
        Boucle recherche (DuckDuckGo via ddgs, gratuit/illimité) -> visite de
        pages comme un navigateur -> évaluation par le modèle (via Omniroute)
        -> synthèse finale.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0 Safari/537.36"
        }

        # --- Recherche ---
        try:
            raw_results = DDGS().text(query, max_results=max_pages)
        except Exception as e:
            raise NoResponseError(f"askWebModel: recherche échouée pour '{query}' ({e})")

        candidates = [
            {"title": r.get("title", ""), "url": r.get("href", "")}
            for r in raw_results if r.get("href")
        ]

        if not candidates:
            raise NoResponseError(f"askWebModel: aucun résultat pour '{query}'")

        # --- Boucle visite + évaluation ---
        visited = []

        for candidate in candidates:
            try:
                page_response = requests.get(candidate["url"], headers=headers, timeout=8)
                page_response.raise_for_status()
            except requests.RequestException:
                continue

            page_soup = BeautifulSoup(page_response.text, "html.parser")
            for tag in page_soup(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.decompose()

            page_text = " ".join(page_soup.get_text(separator=" ").split())[:3000]
            if not page_text:
                continue

            visited.append({
                "title": candidate["title"],
                "url": candidate["url"],
                "text": page_text
            })

            judge_prompt = f"""
Demande de l'utilisateur : {query}

Pages visitées jusqu'ici :
{chr(10).join(f"- {p['title']} ({p['url']}): {p['text'][:500]}" for p in visited)}

Réponds UNIQUEMENT par "OUI" si ces informations suffisent pour répondre
correctement et complètement à la demande, sinon réponds UNIQUEMENT "NON".
"""
            verdict = Model.askModel(
                [{"role": "user", "content": judge_prompt}],
                lambda r: r.strip().upper() in ("OUI", "NON")
            )

            if "OUI" in verdict.strip().upper():
                break

        if not visited:
            raise NoResponseError(f"askWebModel: aucune page accessible pour '{query}'")

        # --- Synthèse finale ---
        final_prompt = f"""
Demande de l'utilisateur : {query}

Informations collectées en visitant plusieurs pages web :
{chr(10).join(f"- {p['title']} ({p['url']}): {p['text']}" for p in visited)}

Réponds à la demande de l'utilisateur en te basant uniquement sur ces
informations. Cite la source (URL) quand c'est pertinent.
"""
        return Model.askModel(
            [{"role": "user", "content": final_prompt}],
            Model.Verification.rawResponse
        )

    

    
    class Verification:
        def isJson( object ):
            try:
                json.loads( object )
                return True
            except JSONDecodeError:
                return False
        
        def isPath( path ):
            return os.path.exists( path )

        def isLink( link ):
            if link.find( "http" ) == 0:
                return True
            if link.find( "www" ) != -1:
                return True
        
        def rawResponse( a ):
            if len( a ) != 0:
                return True
            return False


    # def askModel(model: str, message, thinking: str = "high", max_retries: int = MAX_RETRIES, verification=None) -> str:
    #     """
    #     Interface unique pour interroger un modèle.
    #     Détermine si l'appel doit passer par Groq ou Ollama.
    #     """
    #     if verification is None:
    #         verification = Model.Verification.rawResponse

    #     if model == OLLAMA_MODEL:
    #         if not isinstance(message, list):
    #             message = [message]
    #         return Model.askOllamaModel(model, message)

    #     return Model.askGroqModel(model, message, thinking, max_retries, verification)

    # def askOllamaModel(model: str, conversation: List[Dict[str, str]]) -> str:
    #     # print( "asking ollama" )
    #     global ollama_client
    #     """
    #     Envoie une requête de chat à un modèle Ollama local en utilisant l'historique de la conversation.

    #     Args:
    #         model (str): Le nom du modèle à utiliser (ex: "llama2", "mistral").
    #         conversation (List[Dict[str, str]]): La liste des messages de conversation.
    #             Chaque élément doit être un dictionnaire avec 'role' et 'content'.
    #             Exemple: [{"role": "user", "content": "Bonjour"}, {"role": "assistant", "content": "Salut !"}]

    #     Returns:
    #         str: La réponse générée par le modèle, ou un message d'erreur.
    #     """
    #     if ollama_client is None:
    #         return "ERREUR: Impossible de se connecter au client Ollama. Veuillez vérifier que le serveur est lancé."
        
    #     if model is None:
    #         return "ERREUR: Veuillez spécifier un modèle."

    #     # print(f"\n🤖 Envoi de la requête au modèle '{model}'...")

    #     try:
    #         # Utilisation de client.chat() pour envoyer l'historique complet
    #         response = ollama_client.chat(
    #             model=model,
    #             messages=conversation
    #         )
            
    #         # Extraction du contenu de la réponse
    #         return response['message']['content']

    #     except Exception as e:
    #         if "model not found" in str(e):
    #             return f"ERREUR: Le modèle '{model}' n'est pas trouvé ou n'est pas téléchargé. Veuillez exécuter 'ollama pull {model}'."
    #         elif "connection error" in str(e) or "connection refused" in str(e):
    #             return "ERREUR DE CONNEXION: Le serveur Ollama semble être arrêté. Veuillez le relancer."
    #         else:
    #             return f"Une erreur inattendue est survenue: {e}"

    # def askGroqModel( model: str, message: dict, thinking: str, max_retries: int, verification ):
    #     reset_count = 0
    #     log(
    #         f"asking model",
    #         {
    #             "model": model,
    #             "message": message,
    #             "thinking": thinking,
    #             "max_retries": max_retries,
    #             "verification": verification.__name__
    #         },
    #         "info"
    #     )
    #     # log( f"Asking model", f"{model=}, {message=}, {thinking=}, {max_retries=}, {verification.__name__}", "info" )
    #     global clients, WIFI
    #     can_think = False
    #     can_web_search = True if model == WEB_MODEL else False
    #     # print( f"{model=}, {can_web_search=}" )
    #     if not WIFI:
    #         log( "No internet connection", "Asking ollama model instead of groq", "warning" )
    #         can_web_search = False
    #     ans = ""
    #     for i in range( max_retries ):
    #         try:
    #             if WIFI:
    #                 client = Model.getNextClient()
    #                 log( "Asking client groq", {"api-key": client.api_key}, "info" )
                    
    #                 # Préparer les paramètres de la requête
    #                 request_params = {
    #                     "model": model,
    #                     "messages": message
    #                 }
                    
    #                 # Ajouter les paramètres optionnels selon les conditions
    #                 if can_think:
    #                     request_params["reasoning_effort"] = thinking
    #                 if can_web_search:
    #                     request_params["tools"] = [{"type": "browser_search"}]
                    
    #                 # Faire l'appel à l'API
    #                 # print( "asking groq" )
    #                 response = client.chat.completions.create(**request_params)
    #                 print( "response given" )
                    
    #                 # Logger la réponse complète pour déboguer
    #                 log(
    #                     "Full API response",
    #                     {
    #                         "choices_count": len(response.choices) if response.choices else 0,
    #                         "first_choice": str(response.choices[0]) if response.choices else None,
    #                         "message": str(response.choices[0].message) if response.choices else None,
    #                         "content": response.choices[0].message.content if response.choices and response.choices[0].message else None
    #                     },
    #                     "debug"
    #                 )
                    
    #                 ans = response.choices[0].message.content
    #                 # print( "logged" )
    #             else:
    #                 # print( "asking ollama..." )
    #                 ans = Model.askOllamaModel( OLLAMA_MODEL, message )
    #                 # print( "response given" )
    #             # print( "verification" )
    #             # Vérifier si la réponse est vide et logger les détails
    #             if not ans or ans.strip() == "":
    #                 log(
    #                     "Empty response from model",
    #                     {
    #                         "model": model,
    #                         "response": ans,
    #                         "response_length": len(ans) if ans else 0
    #                     },
    #                     "warning"
    #                 )
    #             if verification.__name__ == "isJson":
    #                 ans = ans.replace( "```json", '' ).replace( "```", '' )
    #             log(
    #                 "Verifying if response is correct",
    #                 {
    #                     "response": ans,
    #                     "verification": verification.__name__
    #                 },
    #                 "info"
    #             )
    #             # print( "final verification" )
    #             if not verification( ans ):
    #                 print( "verification didn't match" )
    #                 raise NotValidResponse( f"The ai's response doesn't match or respect the output specifications. Verification : {verification.__name__}, response is {ans}" )
    #             # print( "return..." )
    #             return ans
    #         except BadRequestError as e:
    #             log(
    #                 f"Wrong request for model",
    #                 {
    #                     "error": str( e ),
    #                     "response": ans,
    #                     "message": message
    #                 },
    #                 "warning"
    #             )
    #             print( str( e ) )
    #             can_web_search = False
    #         except APIStatusError as e:
    #             log(
    #                 f"Invalid response from API",
    #                 {
    #                     "error": str( e ),
    #                     "response": ans,
    #                     "message": message
    #                 },
    #                 "error"
    #             )
    #             print( str( e ) )
    #             if str( e ).find( "reasoning_effort" ) != -1 and str( e ).find( "not supported" ) != -1:
    #                 can_think = False
    #             if model == MAIN_MODEL:
    #                 if e.status_code == 413 and str( e ).lower().find( "request too large for model" ) != -1:
    #                     reset_count += 1
    #                     if client_max - 2 <= 0:
    #                         if reset_count == client_max:
    #                             reset_count = 0
    #                             autoEraseConversation()
    #                     else:
    #                         if reset_count == client_max - 2:
    #                             reset_count = 0
    #                             autoEraseConversation()
    #         except NotValidResponse as e:
    #             print( str( e ) )
    #             log(
    #                 f"Invalid response from model",
    #                 {
    #                     "error": str( e ),
    #                     "response": ans,
    #                     "message": message
    #                 },
    #                 "warning"
    #             )
    #     if ans and ans.strip():
    #         return ans

    #     # Si toutes les tentatives Groq échouent, tenter un fallback vers Ollama.
    #     if model != OLLAMA_MODEL:
    #         log(
    #             "Groq fallback",
    #             {
    #                 "model": model,
    #                 "message": message,
    #                 "attempts": max_retries
    #             },
    #             "warning"
    #         )
    #         ollama_conversation = message if isinstance(message, list) else [message]
    #         ollama_ans = Model.askOllamaModel(OLLAMA_MODEL, ollama_conversation, max_retries, verification)
    #         if ollama_ans and ollama_ans.strip():
    #             if verification.__name__ == "isJson":
    #                 ollama_ans = ollama_ans.replace("```json", "").replace("```", "")
    #             if verification(ollama_ans):
    #                 return ollama_ans
    #             log(
    #                 "Ollama fallback response failed verification",
    #                 {
    #                     "response": ollama_ans,
    #                     "verification": verification.__name__
    #                 },
    #                 "warning"
    #             )
    #         else:
    #             log(
    #                 "Ollama fallback returned empty response",
    #                 {
    #                     "response": ollama_ans,
    #                     "model": OLLAMA_MODEL
    #                 },
    #                 "warning"
    #             )

    #     # Si toutes les tentatives échouent, retourner la dernière réponse ou un message d'erreur
    #     raise NoResponseError( f"Le modèle n'a pas répondu de réponse valide après {max_retries} essais" )
    
    # def getNextClient():
    #     global client_max, client_index, clients
    #     client = clients[client_index]
    #     client_index += 1
    #     if client_index == client_max:
    #         client_index = 0
    #     return client


loadPrint()#c

# =====================
# IMAGE TO BASE64
# =====================
def image_to_base64( path ):
    path = path.replace( '"', '' )
    with open( path, "rb" ) as f:
        return base64.b64encode( f.read() ).decode()

loadPrint()#c

# def webSearch( query: str ):
#     for i in range( MAX_RETRIES ):
#         try:
#             result = Model.askModel(
#                 WEB_MODEL,
#                 [
#                     {
#                         "role": "system",
#                         "content": "Va chercher sur internet la réponse à la question de l'utilisateur."
#                     },
#                     {
#                         "role": "user",
#                         "content": query
#                     }
#                 ],
#                 "high",
#                 MAX_RETRIES,
#                 Model.Verification.rawResponse
#             )
#             print( result )
#             return result, True
#         except NoResponseError as e:
#             result = str( e )
#     return result, True

def webSearch(query):
    """
    Recherche web pour une IA.

    Args:
        query (str): Recherche à effectuer
        max_results (int): Nombre de résultats retournés

    Returns:
        list: Résultats avec titre, lien et description
    """

    return Model.askWebModel( query ), True

    # results = []

    # try:
    #     with DDGS() as ddgs:
    #         search_results = ddgs.text(
    #             query,
    #             max_results=max_results
    #         )

    #         for r in search_results:
    #             results.append({
    #                 "title": r.get("title"),
    #                 "url": r.get("href"),
    #                 "content": r.get("body")
    #             })

    # except Exception as e:
    #     return {
    #         "error": str(e)
    #     }

    # return results

loadPrint()#c

def rms(audio: np.ndarray) -> float:
    return float(np.sqrt(np.mean(audio ** 2)))

loadPrint()#c

def get_default_wasapi_loopback_device(p: pyaudiowpatch.PyAudio) -> dict | None:
    try:
        return p.get_default_wasapi_loopback()
    except Exception:
        pass
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev.get("isLoopbackDevice", False):
            return dev
    return None

loadPrint()#c

def _record_stream_callback(frames_holder: list, num_chunks_target: int, done_event: threading.Event):
    """Retourne un callback PyAudio qui accumule les frames."""
    def callback(in_data, frame_count, time_info, status):
        frames_holder.append(in_data)
        if len(frames_holder) >= num_chunks_target:
            done_event.set()
            return (None, pyaudiowpatch.paComplete)
        return (None, pyaudiowpatch.paContinue)
    return callback

loadPrint()#c

def bandChart(title, data, title_x_axis, title_y_axis, x_pos=100, y_pos=100):
    """
    Crée et affiche un diagramme en barres interactif.
    La taille s'adapte automatiquement au nombre de barres et à la longueur des labels.
    Non-bloquant : s'exécute dans un thread séparé et retourne immédiatement.

    Raccourcis clavier (widget en focus) :
        Ctrl+C  -> copie une capture PNG transparent dans le presse-papiers
        Ctrl+X  -> idem + ferme le widget
    """

    def _run():
        # ── Calcul automatique des dimensions ────────────────────────────────
        # Fenêtre temporaire pour mesurer les polices avant de créer le widget
        _tmp        = tk.Tk()
        _tmp.withdraw()
        _label_font = font.Font(family='Helvetica', size=10)
        _title_font = font.Font(family='Helvetica', size=14, weight='bold')

        max_label_w = max(_label_font.measure(str(k)) for k in data.keys())
        title_w     = _title_font.measure(title)
        max_val_tmp = max(data.values())
        y_max_tmp   = (int(max_val_tmp * 2) + 1) / 2.0
        grad_w      = max(_label_font.measure(f"{i * y_max_tmp / 5:.2f}") for i in range(6))
        _tmp.destroy()

        TITLE_BAR_H   = 24
        MARGIN_LEFT   = int(grad_w) + 30
        MARGIN_RIGHT  = 20
        MARGIN_TOP    = 60 + TITLE_BAR_H
        MARGIN_BOTTOM = max(50, int(max_label_w) + 20)

        # Largeur par barre : basée sur le label le plus long, entre 60 et 120 px
        BAR_SLOT = max(60, min(120, int(max_label_w) + 20))
        chart_w  = BAR_SLOT * len(data)
        chart_w  = max(chart_w, int(title_w) + 40)

        WIN_W = MARGIN_LEFT + chart_w + MARGIN_RIGHT
        WIN_H = 420

        # ── Fenêtre fantôme (porte l'icône taskbar) ───────────────────────────
        # overrideredirect supprime l'icône taskbar ET bloque ImageGrab.
        # Solution : une fenêtre parent native (avec décoration) minuscule,
        # cachée hors écran, qui porte le titre et l'icône dans la taskbar.
        ghost = tk.Tk()
        ghost.title(title)
        ghost.geometry(f"1x1+-32000+-32000")   # hors écran
        ghost.resizable(False, False)
        # On la rend invisible visuellement mais elle reste dans la taskbar
        ghost.attributes('-alpha', 0.01)        # quasi transparent
        ghost.configure(bg='black')

        # ── Fenêtre principale (widget flottant) ──────────────────────────────
        root = tk.Toplevel(ghost)
        root.title(title)
        root.geometry(f"{WIN_W}x{WIN_H}+{x_pos}+{y_pos}")
        root.configure(bg='black')
        root.overrideredirect(True)
        root.transient(ghost)   # lie les deux fenêtres

        # ── Drag ─────────────────────────────────────────────────────────────
        drag_state = {"x": 0, "y": 0, "dragging": False}

        def on_drag_start(event):
            drag_state["x"] = event.x_root
            drag_state["y"] = event.y_root
            drag_state["dragging"] = True

        def on_drag_motion(event):
            if not drag_state["dragging"]:
                return
            dx = event.x_root - drag_state["x"]
            dy = event.y_root - drag_state["y"]
            drag_state["x"] = event.x_root
            drag_state["y"] = event.y_root
            root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

        def on_drag_stop(event):
            drag_state["dragging"] = False

        # ── Win32 : transparence couleur-clé ──────────────────────────────────
        root.update_idletasks()
        hwnd = root.winfo_id()
        ghost_hwnd = ghost.winfo_id()

        if sys.platform.startswith('win'):
            # Fenêtre principale : transparence + toolwindow (pas dans taskbar)
            style_ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            style_ex = (style_ex | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW) \
                       & ~win32con.WS_EX_APPWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style_ex)
            win32gui.SetLayeredWindowAttributes(
                hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
            )

            # Fenêtre fantôme : forcer APPWINDOW pour avoir l'icône taskbar
            ghost_style = win32gui.GetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE)
            ghost_style = (ghost_style | win32con.WS_EX_APPWINDOW) \
                          & ~win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE, ghost_style)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_HIDE)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_SHOW)

        def bring_to_front(event=None):
            """Remet le widget au premier plan (clic sur icône taskbar)."""
            try:
                root.lift()
                root.focus_force()
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                )
            except Exception:
                pass

        # Clic sur l'icône taskbar -> ghost reçoit <Map> ou <FocusIn>
        ghost.bind("<Map>", bring_to_front)
        ghost.bind("<FocusIn>", bring_to_front)

        def close_all():
            root.destroy()
            ghost.destroy()

        # ── Canvas ────────────────────────────────────────────────────────────
        canvas = tk.Canvas(root, width=WIN_W, height=WIN_H, bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        # ── Barre de titre (drag handle) ──────────────────────────────────────
        TITLE_BAR_H = 24
        title_bar = canvas.create_rectangle(
            0, 0, WIN_W, TITLE_BAR_H,
            fill='#1a1a1a', outline='#333333', width=1
        )
        title_bar_label = canvas.create_text(
            WIN_W / 2, TITLE_BAR_H / 2,
            text=title, fill="#AAAAAA",
            font=font.Font(family='Helvetica', size=9)
        )

        for item in (title_bar, title_bar_label):
            canvas.tag_bind(item, "<ButtonPress-1>",  on_drag_start)
            canvas.tag_bind(item, "<B1-Motion>",       on_drag_motion)
            canvas.tag_bind(item, "<ButtonRelease-1>", on_drag_stop)

        # ── Bouton X ──────────────────────────────────────────────────────────
        CLOSE_SIZE = 18
        CLOSE_X    = WIN_W - CLOSE_SIZE - 4
        CLOSE_Y    = 3
        close_btn  = canvas.create_rectangle(
            CLOSE_X, CLOSE_Y,
            CLOSE_X + CLOSE_SIZE, CLOSE_Y + CLOSE_SIZE,
            fill='#cc3333', outline='', width=0
        )
        canvas.create_text(
            CLOSE_X + CLOSE_SIZE / 2, CLOSE_Y + CLOSE_SIZE / 2,
            text="X", fill="white",
            font=font.Font(family='Helvetica', size=9, weight='bold')
        )

        def on_click(event):
            if (CLOSE_X <= event.x <= CLOSE_X + CLOSE_SIZE and
                    CLOSE_Y <= event.y <= CLOSE_Y + CLOSE_SIZE):
                close_all()

        def on_hover(event):
            inside = (CLOSE_X <= event.x <= CLOSE_X + CLOSE_SIZE and
                      CLOSE_Y <= event.y <= CLOSE_Y + CLOSE_SIZE)
            canvas.itemconfig(close_btn, fill='#ff5555' if inside else '#cc3333')

        canvas.bind("<ButtonPress-1>", on_click)
        canvas.bind("<Motion>", on_hover)

        # ── Marges graphique (déjà calculées plus haut) ───────────────────────
        chart_width  = WIN_W - MARGIN_LEFT - MARGIN_RIGHT
        chart_height = WIN_H - MARGIN_TOP  - MARGIN_BOTTOM

        canvas.create_line(MARGIN_LEFT, MARGIN_TOP,
                           MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)
        canvas.create_line(MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           WIN_W - MARGIN_RIGHT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)

        title_font    = font.Font(family='Helvetica', size=14, weight='bold')
        label_font    = font.Font(family='Helvetica', size=10)
        chart_title_y = TITLE_BAR_H + (MARGIN_TOP - TITLE_BAR_H) / 2

        canvas.create_text(WIN_W / 2, chart_title_y,
                           text=title, fill="#FFFFFF", font=title_font)
        canvas.create_text(WIN_W / 2, WIN_H - MARGIN_BOTTOM / 3,
                           text=title_x_axis, fill="#FFFFFF", font=label_font)
        canvas.create_text(MARGIN_LEFT / 3, WIN_H / 2,
                           text=title_y_axis, fill="#FFFFFF", font=label_font, angle=90)

        max_val = max(data.values())
        y_max   = (int(max_val * 2) + 1) / 2.0
        step    = y_max / 5
        for i in range(6):
            y_val = i * step
            y = MARGIN_TOP + chart_height - (y_val / y_max) * chart_height
            canvas.create_line(MARGIN_LEFT - 5, y, MARGIN_LEFT, y, fill="#FFFFFF", width=1)
            canvas.create_text(MARGIN_LEFT - 10, y,
                               text=f"{y_val:.2f}", fill="#FFFFFF",
                               font=label_font, anchor='e')

        # ── Barres ────────────────────────────────────────────────────────────
        num_bars    = len(data)
        bar_spacing = BAR_SLOT          # 1 slot par barre, déjà calculé
        bar_width   = bar_spacing * 0.6
        bars        = []

        for idx, (label, value) in enumerate(data.items()):
            x_center = MARGIN_LEFT + bar_spacing * (idx + 0.5)
            x0, x1   = x_center - bar_width / 2, x_center + bar_width / 2
            rect_id  = canvas.create_rectangle(
                x0, WIN_H - MARGIN_BOTTOM,
                x1, WIN_H - MARGIN_BOTTOM,
                fill='#{:02x}{:02x}{:02x}'.format(*THEME_COLOR),
                width=0
            )
            bars.append((rect_id, value))
            canvas.create_text(x_center, WIN_H - MARGIN_BOTTOM + 15,
                               text=label, fill="#FFFFFF",
                               font=label_font, anchor='n')

        # ── Capture PNG transparent via PrintWindow (Win32) ──────────────────
        def capture_transparent_png():
            """
            Utilise PrintWindow() pour rendre la fenêtre dans un bitmap GDI,
            même si elle est derrière d'autres fenêtres ou overrideredirect.
            Aucune dépendance à Ghostscript.
            Le fond noir (couleur-clé) devient transparent.
            """
            root.update_idletasks()

            # Créer un DC compatible et un bitmap de la taille de la fenêtre
            hwnd_dc  = win32gui.GetWindowDC(hwnd)
            mfc_dc   = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc  = mfc_dc.CreateCompatibleDC()
            bmp      = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfc_dc, WIN_W, WIN_H)
            save_dc.SelectObject(bmp)

            # PrintWindow : demande à la fenêtre de se dessiner dans le DC
            # PW_RENDERFULLCONTENT (0x2) force le rendu complet sous Win8+
            PW_RENDERFULLCONTENT = 0x2
            ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)

            # Convertir le bitmap GDI en image Pillow
            bmp_info = bmp.GetInfo()
            bmp_bits = bmp.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGB',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_bits, 'raw', 'BGRX', 0, 1
            ).convert("RGBA")

            # Libérer les ressources GDI
            win32gui.DeleteObject(bmp.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)

            # Remplacer les pixels noirs (fond couleur-clé) par transparent
            pixels   = img.load()
            w, h     = img.size
            TOLERANCE = 15
            for py in range(h):
                for px in range(w):
                    r, g, b, a = pixels[px, py]
                    if r <= TOLERANCE and g <= TOLERANCE and b <= TOLERANCE:
                        pixels[px, py] = (0, 0, 0, 0)
            return img

        def copy_to_clipboard(img):
            """
            Copie en deux formats :
              PNG  -> préserve la transparence (Discord, Slack, navigateurs)
              DIB  -> compatibilité (Word, Paint, etc.)
            """
            png_buf = io.BytesIO()
            img.save(png_buf, format="PNG")
            png_data = png_buf.getvalue()

            CF_PNG = win32clipboard.RegisterClipboardFormat("PNG")

            dib_buf = io.BytesIO()
            bg = Image.new("RGB", img.size, (0, 0, 0))
            bg.paste(img, mask=img.split()[3])
            bg.save(dib_buf, format="BMP")
            dib_data = dib_buf.getvalue()[14:]

            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(CF_PNG, png_data)
                win32clipboard.SetClipboardData(win32con.CF_DIB, dib_data)
            finally:
                win32clipboard.CloseClipboard()

        def on_ctrl_c(event=None):
            img = capture_transparent_png()
            copy_to_clipboard(img)

        def on_ctrl_x(event=None):
            img = capture_transparent_png()
            copy_to_clipboard(img)
            root.after(50, close_all)

        root.bind("<Control-c>", on_ctrl_c)
        root.bind("<Control-x>", on_ctrl_x)
        ghost.bind("<Control-c>", on_ctrl_c)
        ghost.bind("<Control-x>", on_ctrl_x)

        # ── Animation (easing exponentiel) ────────────────────────────────────
        DELAY_MS        = 16
        EASE            = 0.08
        THRESHOLD       = 0.5
        current_heights = [0.0] * len(bars)

        def animate():
            done = True
            for i, (rect_id, target_val) in enumerate(bars):
                target_h = (target_val / y_max) * chart_height
                diff     = target_h - current_heights[i]
                if abs(diff) < THRESHOLD:
                    current_heights[i] = target_h
                else:
                    current_heights[i] += diff * EASE
                    done = False
                y_top  = MARGIN_TOP + chart_height - current_heights[i]
                coords = canvas.coords(rect_id)
                canvas.coords(rect_id, coords[0], y_top, coords[2], WIN_H - MARGIN_BOTTOM)
            if not done:
                root.after(DELAY_MS, animate)

        root.after(200, animate)
        ghost.mainloop()

    threading.Thread(target=_run, daemon=True).start()

loadPrint()#c

def _generate_shades(base_rgb, n):
    """
    Génère n teintes à partir de la couleur thème.
    On fait varier la luminosité et légèrement la saturation en HSV.
    """
    import colorsys
    r, g, b = [x / 255.0 for x in base_rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    shades = []
    for i in range(n):
        # Répartir les teintes : alterner luminosité + décaler légèrement la teinte
        t        = i / max(n - 1, 1)
        new_h    = (h + t * 0.18) % 1.0        # légère rotation de teinte
        new_s    = max(0.3, s - t * 0.25)       # désaturation progressive
        new_v    = 0.95 - t * 0.45              # de lumineux à sombre
        nr, ng, nb = colorsys.hsv_to_rgb(new_h, new_s, new_v)
        shades.append('#{:02x}{:02x}{:02x}'.format(
            int(nr * 255), int(ng * 255), int(nb * 255)
        ))
    return shades

loadPrint()#c

def pieChart(title, data, x_pos=100, y_pos=100):
    """
    Crée et affiche un diagramme circulaire (camembert) interactif.
    Non-bloquant : s'exécute dans un thread séparé et retourne immédiatement.

    Les proportions sont calculées automatiquement sur la somme totale des valeurs
    (peu importe que la somme soit 100, 360, 5000, etc.)

    Chaque part affiche son pourcentage à l'intérieur, près du bord,
    et son label à l'extérieur avec une ligne de repère.

    Raccourcis clavier (widget en focus) :
        Ctrl+C  -> copie une capture PNG transparent dans le presse-papiers
        Ctrl+X  -> idem + ferme le widget

    Args:
        title (str): Titre principal du diagramme
        data (dict): Dictionnaire {label: valeur}
        x_pos (int): Position X de la fenêtre (défaut: 100)
        y_pos (int): Position Y de la fenêtre (défaut: 100)
    """

    def _run():
        # ── Mesure des labels pour calculer la marge nécessaire ─────────────
        _tmp        = tk.Tk()
        _tmp.withdraw()
        _label_font = font.Font(family='Helvetica', size=9)
        _title_font = font.Font(family='Helvetica', size=14, weight='bold')

        max_label_w = max(_label_font.measure(str(k)) for k in data.keys())
        title_w     = _title_font.measure(title)
        _tmp.destroy()

        # ── Dimensions ───────────────────────────────────────────────────────
        TITLE_BAR_H  = 24
        LINE_OUT     = 30    # longueur de la ligne de repère
        TEXT_PAD     = 6     # espace entre la fin de la ligne et le bord du texte
        # Marge = ligne de repère + largeur max du label + padding
        LABEL_MARGIN = LINE_OUT + int(max_label_w) + TEXT_PAD + 10
        LABEL_MARGIN = max(LABEL_MARGIN, 90)   # minimum confortable

        PIE_SIZE = 340
        WIN_W    = max(PIE_SIZE + LABEL_MARGIN * 2, int(title_w) + 40)
        WIN_H    = PIE_SIZE + LABEL_MARGIN * 2 + TITLE_BAR_H + 40

        CX = WIN_W / 2
        CY = TITLE_BAR_H + 40 + LABEL_MARGIN + PIE_SIZE / 2
        R  = PIE_SIZE / 2

        # ── Fenêtre fantôme (porte l'icône taskbar) ───────────────────────────
        ghost = tk.Tk()
        ghost.title(title)
        ghost.geometry("1x1+-32000+-32000")
        ghost.resizable(False, False)
        ghost.attributes('-alpha', 0.01)
        ghost.configure(bg='black')

        # ── Fenêtre principale ────────────────────────────────────────────────
        root = tk.Toplevel(ghost)
        root.title(title)
        root.geometry(f"{WIN_W}x{WIN_H}+{x_pos}+{y_pos}")
        root.configure(bg='black')
        root.overrideredirect(True)
        root.transient(ghost)

        # ── Drag ──────────────────────────────────────────────────────────────
        drag_state = {"x": 0, "y": 0}

        def on_drag_start(event):
            drag_state["x"] = event.x_root
            drag_state["y"] = event.y_root

        def on_drag_motion(event):
            dx = event.x_root - drag_state["x"]
            dy = event.y_root - drag_state["y"]
            drag_state["x"] = event.x_root
            drag_state["y"] = event.y_root
            root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

        # ── Win32 setup ───────────────────────────────────────────────────────
        root.update_idletasks()
        hwnd       = root.winfo_id()
        ghost_hwnd = ghost.winfo_id()

        if sys.platform.startswith('win'):
            style_ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            style_ex = (style_ex | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW) \
                       & ~win32con.WS_EX_APPWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style_ex)
            win32gui.SetLayeredWindowAttributes(
                hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
            )
            ghost_style = win32gui.GetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE)
            ghost_style = (ghost_style | win32con.WS_EX_APPWINDOW) \
                          & ~win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE, ghost_style)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_HIDE)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_SHOW)

        def bring_to_front(event=None):
            try:
                root.lift()
                root.focus_force()
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                )
            except Exception:
                pass

        ghost.bind("<Map>", bring_to_front)
        ghost.bind("<FocusIn>", bring_to_front)

        def close_all():
            root.destroy()
            ghost.destroy()

        # ── Canvas ────────────────────────────────────────────────────────────
        canvas = tk.Canvas(root, width=WIN_W, height=WIN_H,
                           bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        # ── Barre de titre ────────────────────────────────────────────────────
        title_bar = canvas.create_rectangle(
            0, 0, WIN_W, TITLE_BAR_H,
            fill='#1a1a1a', outline='#333333', width=1
        )
        title_bar_lbl = canvas.create_text(
            WIN_W / 2, TITLE_BAR_H / 2,
            text=title, fill="#AAAAAA",
            font=font.Font(family='Helvetica', size=9)
        )
        for item in (title_bar, title_bar_lbl):
            canvas.tag_bind(item, "<ButtonPress-1>",  on_drag_start)
            canvas.tag_bind(item, "<B1-Motion>",       on_drag_motion)

        # ── Bouton X ──────────────────────────────────────────────────────────
        CLOSE_SIZE = 18
        CLOSE_X    = WIN_W - CLOSE_SIZE - 4
        CLOSE_Y    = 3
        close_btn  = canvas.create_rectangle(
            CLOSE_X, CLOSE_Y,
            CLOSE_X + CLOSE_SIZE, CLOSE_Y + CLOSE_SIZE,
            fill='#cc3333', outline='', width=0
        )
        canvas.create_text(
            CLOSE_X + CLOSE_SIZE / 2, CLOSE_Y + CLOSE_SIZE / 2,
            text="X", fill="white",
            font=font.Font(family='Helvetica', size=9, weight='bold')
        )

        def on_click(event):
            if (CLOSE_X <= event.x <= CLOSE_X + CLOSE_SIZE and
                    CLOSE_Y <= event.y <= CLOSE_Y + CLOSE_SIZE):
                close_all()

        def on_hover(event):
            inside = (CLOSE_X <= event.x <= CLOSE_X + CLOSE_SIZE and
                      CLOSE_Y <= event.y <= CLOSE_Y + CLOSE_SIZE)
            canvas.itemconfig(close_btn, fill='#ff5555' if inside else '#cc3333')

        canvas.bind("<ButtonPress-1>", on_click)
        canvas.bind("<Motion>", on_hover)

        # ── Titre du graphique ────────────────────────────────────────────────
        title_font = font.Font(family='Helvetica', size=14, weight='bold')
        label_font = font.Font(family='Helvetica', size=9)
        pct_font   = font.Font(family='Helvetica', size=9, weight='bold')

        canvas.create_text(
            WIN_W / 2, TITLE_BAR_H + 20,
            text=title, fill="#FFFFFF", font=title_font
        )

        # ── Calcul des parts ──────────────────────────────────────────────────
        labels  = list(data.keys())
        values  = list(data.values())
        total   = sum(values)
        n       = len(values)
        shades  = _generate_shades(THEME_COLOR, n)

        # Angles cibles (en degrés, sens horaire depuis le haut = -90°)
        target_angles = [v / total * 360.0 for v in values]

        # ── Créer les arcs (initialement à 0°) ───────────────────────────────
        # Tkinter create_arc : start=angle de départ (0=est), extent=amplitude
        # On part du haut (-90°) et on tourne dans le sens horaire (extent négatif)
        arc_ids      = []
        label_ids    = []   # (line_id, label_id, pct_id)
        current_start = -90.0   # départ en haut

        for i in range(n):
            arc_id = canvas.create_arc(
                CX - R, CY - R, CX + R, CY + R,
                start=current_start,
                extent=0,           # commence à 0, l'animation va l'étendre
                fill=shades[i],
                outline='#000000',
                width=1,
                style=tk.PIESLICE
            )
            arc_ids.append(arc_id)
            current_start -= target_angles[i]   # avance pour la prochaine part

        # Labels extérieurs et pourcentages intérieurs (créés vides, positionnés après animation)
        for i in range(n):
            pct_val  = values[i] / total * 100.0
            line_id  = canvas.create_line(0, 0, 0, 0, fill="#888888", width=1)
            lbl_id   = canvas.create_text(0, 0, text=labels[i],
                                          fill="#FFFFFF", font=label_font,
                                          anchor='center')
            pct_id   = canvas.create_text(0, 0,
                                          text=f"{pct_val:.1f}%",
                                          fill="#000000", font=pct_font,
                                          anchor='center')
            label_ids.append((line_id, lbl_id, pct_id))

        def place_labels(extents):
            """
            Place les labels extérieurs et les % intérieurs
            en fonction des angles courants.
            """
            start_deg = -90.0
            for i in range(n):
                ext = extents[i]
                mid_deg = start_deg - ext / 2.0          # angle du milieu de la part
                mid_rad = math.radians(mid_deg)

                # -- Pourcentage intérieur (à 72% du rayon) --
                pr   = R * 0.72
                px   = CX + pr * math.cos(mid_rad)
                py   = CY - pr * math.sin(mid_rad)
                canvas.coords(label_ids[i][2], px, py)

                # -- Label extérieur avec ligne de repère --
                # Point sur le bord du cercle
                bx = CX + R * math.cos(mid_rad)
                by = CY - R * math.sin(mid_rad)
                # Point intermédiaire (légèrement au-delà)
                mx = CX + (R + 12) * math.cos(mid_rad)
                my = CY - (R + 12) * math.sin(mid_rad)
                # Point final du label (plus loin)
                lx = CX + (R + LINE_OUT) * math.cos(mid_rad)
                ly = CY - (R + LINE_OUT) * math.sin(mid_rad)

                canvas.coords(label_ids[i][0], bx, by, mx, my)

                # Ancre du texte selon le côté du cercle
                cos_v = math.cos(mid_rad)
                if cos_v > 0.15:
                    anchor = 'w'
                elif cos_v < -0.15:
                    anchor = 'e'
                else:
                    anchor = 'center'
                canvas.itemconfig(label_ids[i][1], anchor=anchor)
                canvas.coords(label_ids[i][1], lx, ly)

                start_deg -= ext

        # ── Animation (easing exponentiel sur les extents) ────────────────────
        DELAY_MS        = 16
        EASE            = 0.08
        THRESHOLD       = 0.08   # degrés
        current_extents = [0.0] * n

        def animate():
            done = True
            start_deg = -90.0
            for i in range(n):
                diff = target_angles[i] - current_extents[i]
                if abs(diff) < THRESHOLD:
                    current_extents[i] = target_angles[i]
                else:
                    current_extents[i] += diff * EASE
                    done = False
                canvas.itemconfig(arc_ids[i],
                                  start=start_deg,
                                  extent=-current_extents[i])
                start_deg -= current_extents[i]

            place_labels(current_extents)

            if not done:
                root.after(DELAY_MS, animate)

        root.after(200, animate)

        # ── Capture PNG transparent ───────────────────────────────────────────
        def capture_transparent_png():
            root.update_idletasks()
            hwnd_dc = win32gui.GetWindowDC(hwnd)
            mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            bmp     = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfc_dc, WIN_W, WIN_H)
            save_dc.SelectObject(bmp)
            ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0x2)
            bmp_info = bmp.GetInfo()
            bmp_bits = bmp.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGB',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_bits, 'raw', 'BGRX', 0, 1
            ).convert("RGBA")
            win32gui.DeleteObject(bmp.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            pixels    = img.load()
            w, h      = img.size
            TOLERANCE = 15
            for py in range(h):
                for px in range(w):
                    r, g, b, a = pixels[px, py]
                    if r <= TOLERANCE and g <= TOLERANCE and b <= TOLERANCE:
                        pixels[px, py] = (0, 0, 0, 0)
            return img

        def copy_to_clipboard(img):
            png_buf  = io.BytesIO()
            img.save(png_buf, format="PNG")
            png_data = png_buf.getvalue()
            CF_PNG   = win32clipboard.RegisterClipboardFormat("PNG")
            dib_buf  = io.BytesIO()
            bg = Image.new("RGB", img.size, (0, 0, 0))
            bg.paste(img, mask=img.split()[3])
            bg.save(dib_buf, format="BMP")
            dib_data = dib_buf.getvalue()[14:]
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(CF_PNG, png_data)
                win32clipboard.SetClipboardData(win32con.CF_DIB, dib_data)
            finally:
                win32clipboard.CloseClipboard()

        def on_ctrl_c(event=None):
            copy_to_clipboard(capture_transparent_png())

        def on_ctrl_x(event=None):
            copy_to_clipboard(capture_transparent_png())
            root.after(50, close_all)

        root.bind("<Control-c>", on_ctrl_c)
        root.bind("<Control-x>", on_ctrl_x)
        ghost.bind("<Control-c>", on_ctrl_c)
        ghost.bind("<Control-x>", on_ctrl_x)

        ghost.mainloop()

    threading.Thread(target=_run, daemon=True).start()

loadPrint()#c

def lineChart(title, data, title_x_axis, title_y_axis, x_pos=100, y_pos=100):
    """
    Diagramme à ligne brisée interactif.
    data = {label_x: valeur, ...} — points dans l'ordre d'insertion.
    Non-bloquant. Ctrl+C = copie PNG transparent, Ctrl+X = copie + ferme.
    """

    def _run():

        # ── Mesure des polices pour dimensionner la fenêtre ──────────────────
        _tmp        = tk.Tk()
        _tmp.withdraw()
        _lf  = font.Font(family='Helvetica', size=10)
        _tf  = font.Font(family='Helvetica', size=14, weight='bold')

        max_label_w = max(_lf.measure(str(k)) for k in data.keys())
        title_w     = _tf.measure(title)
        min_val     = min(data.values())
        max_val     = max(data.values())

        # Calcul de l'échelle Y (même logique que bandChart)
        val_range   = max_val - min_val if max_val != min_val else max_val
        raw_top     = max_val + val_range * 0.1
        y_max       = (int(raw_top * 2) + 1) / 2.0
        y_min       = min(0.0, min_val)
        grad_w      = max(_lf.measure(f"{y_min + i * (y_max - y_min) / 5:.2f}") for i in range(6))
        _tmp.destroy()

        TITLE_BAR_H   = 24
        MARGIN_LEFT   = int(grad_w) + 30
        MARGIN_RIGHT  = max(int(max_label_w) // 2 + 10, 20)  # dernière étiquette X peut dépasser
        MARGIN_TOP    = 60 + TITLE_BAR_H
        MARGIN_BOTTOM = max(50, int(max_label_w) + 20)

        PT_SLOT = max(60, min(120, int(max_label_w) + 20))
        chart_w = PT_SLOT * len(data)
        chart_w = max(chart_w, int(title_w) + 40)

        WIN_W = MARGIN_LEFT + chart_w + MARGIN_RIGHT
        WIN_H = 420

        # ── Fenêtre fantôme (icône taskbar) ───────────────────────────────────
        ghost = tk.Tk()
        ghost.title(title)
        ghost.geometry("1x1+-32000+-32000")
        ghost.resizable(False, False)
        ghost.attributes('-alpha', 0.01)
        ghost.configure(bg='black')

        root = tk.Toplevel(ghost)
        root.title(title)
        root.geometry(f"{WIN_W}x{WIN_H}+{x_pos}+{y_pos}")
        root.configure(bg='black')
        root.overrideredirect(True)
        root.transient(ghost)

        # ── Drag ──────────────────────────────────────────────────────────────
        drag_state = {"x": 0, "y": 0, "dragging": False}

        def on_drag_start(e):
            drag_state["x"] = e.x_root
            drag_state["y"] = e.y_root
            drag_state["dragging"] = True

        def on_drag_motion(e):
            if not drag_state["dragging"]:
                return
            dx = e.x_root - drag_state["x"]
            dy = e.y_root - drag_state["y"]
            drag_state["x"] = e.x_root
            drag_state["y"] = e.y_root
            root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

        def on_drag_stop(e):
            drag_state["dragging"] = False

        # ── Win32 ─────────────────────────────────────────────────────────────
        root.update_idletasks()
        hwnd       = root.winfo_id()
        ghost_hwnd = ghost.winfo_id()

        if sys.platform.startswith('win'):
            sx = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            sx = (sx | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW) \
                 & ~win32con.WS_EX_APPWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, sx)
            win32gui.SetLayeredWindowAttributes(
                hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

            gx = win32gui.GetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE)
            gx = (gx | win32con.WS_EX_APPWINDOW) & ~win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE, gx)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_HIDE)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_SHOW)

        def bring_to_front(e=None):
            try:
                root.lift(); root.focus_force()
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            except Exception:
                pass

        ghost.bind("<Map>",      bring_to_front)
        ghost.bind("<FocusIn>",  bring_to_front)

        def close_all():
            root.destroy()
            ghost.destroy()

        # ── Canvas ────────────────────────────────────────────────────────────
        canvas = tk.Canvas(root, width=WIN_W, height=WIN_H,
                           bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        # ── Barre de titre ────────────────────────────────────────────────────
        tb  = canvas.create_rectangle(0, 0, WIN_W, TITLE_BAR_H,
                                      fill='#1a1a1a', outline='#333333', width=1)
        tbl = canvas.create_text(WIN_W / 2, TITLE_BAR_H / 2, text=title,
                                 fill="#AAAAAA",
                                 font=font.Font(family='Helvetica', size=9))
        for item in (tb, tbl):
            canvas.tag_bind(item, "<ButtonPress-1>",  on_drag_start)
            canvas.tag_bind(item, "<B1-Motion>",       on_drag_motion)
            canvas.tag_bind(item, "<ButtonRelease-1>", on_drag_stop)

        # ── Bouton X ──────────────────────────────────────────────────────────
        CS = 18
        CX_btn = WIN_W - CS - 4
        CY_btn = 3
        cb = canvas.create_rectangle(CX_btn, CY_btn, CX_btn + CS, CY_btn + CS,
                                     fill='#cc3333', outline='', width=0)
        canvas.create_text(CX_btn + CS / 2, CY_btn + CS / 2, text="X",
                           fill="white",
                           font=font.Font(family='Helvetica', size=9, weight='bold'))

        def on_click(e):
            if CX_btn <= e.x <= CX_btn + CS and CY_btn <= e.y <= CY_btn + CS:
                close_all()

        def on_hover(e):
            inside = CX_btn <= e.x <= CX_btn + CS and CY_btn <= e.y <= CY_btn + CS
            canvas.itemconfig(cb, fill='#ff5555' if inside else '#cc3333')

        canvas.bind("<ButtonPress-1>", on_click)
        canvas.bind("<Motion>",        on_hover)

        # ── Zone graphique ────────────────────────────────────────────────────
        chart_width  = WIN_W - MARGIN_LEFT - MARGIN_RIGHT
        chart_height = WIN_H - MARGIN_TOP  - MARGIN_BOTTOM

        # Axes
        canvas.create_line(MARGIN_LEFT, MARGIN_TOP,
                           MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)
        canvas.create_line(MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           WIN_W - MARGIN_RIGHT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)

        # Polices
        title_font = font.Font(family='Helvetica', size=14, weight='bold')
        label_font = font.Font(family='Helvetica', size=10)

        chart_title_y = TITLE_BAR_H + (MARGIN_TOP - TITLE_BAR_H) / 2
        canvas.create_text(WIN_W / 2, chart_title_y,
                           text=title, fill="#FFFFFF", font=title_font)
        canvas.create_text(WIN_W / 2, WIN_H - MARGIN_BOTTOM / 3,
                           text=title_x_axis, fill="#FFFFFF", font=label_font)
        canvas.create_text(MARGIN_LEFT / 3, WIN_H / 2,
                           text=title_y_axis, fill="#FFFFFF", font=label_font, angle=90)

        # Graduations Y + grille pointillée
        y_range = y_max - y_min
        step    = y_range / 5
        for i in range(6):
            y_val = y_min + i * step
            y_px  = WIN_H - MARGIN_BOTTOM - (y_val - y_min) / y_range * chart_height
            canvas.create_line(MARGIN_LEFT - 5, y_px, MARGIN_LEFT, y_px,
                               fill="#FFFFFF", width=1)
            canvas.create_text(MARGIN_LEFT - 10, y_px,
                               text=f"{y_val:.2f}", fill="#FFFFFF",
                               font=label_font, anchor='e')
            if i > 0:   # grille horizontale légère
                canvas.create_line(MARGIN_LEFT, y_px, WIN_W - MARGIN_RIGHT, y_px,
                                   fill="#333333", width=1, dash=(4, 6))

        # ── Points cibles ─────────────────────────────────────────────────────
        labels  = list(data.keys())
        values  = list(data.values())
        n       = len(values)
        TC      = '#{:02x}{:02x}{:02x}'.format(*THEME_COLOR)

        def val_to_px(v):
            """Convertit une valeur en coordonnée Y canvas."""
            return WIN_H - MARGIN_BOTTOM - (v - y_min) / y_range * chart_height

        def idx_to_x(i):
            """Coordonnée X du i-ème point."""
            return MARGIN_LEFT + PT_SLOT * (i + 0.5)

        # Labels X sous l'axe
        for i, lbl in enumerate(labels):
            canvas.create_text(idx_to_x(i), WIN_H - MARGIN_BOTTOM + 15,
                               text=lbl, fill="#FFFFFF",
                               font=label_font, anchor='n')

        # Segments de ligne (coordonnées initiales superposées sur le 1er point)
        # Ils seront mis à jour à chaque frame d'animation
        # On stocke les segments séparément des points
        seg_ids  = []    # un segment entre point i et i+1
        dot_ids  = []    # cercle plein à chaque point
        val_ids  = []    # label de valeur au-dessus de chaque point

        target_ys = [val_to_px(v) for v in values]
        base_y    = val_to_px(y_min)   # bas du graphique = point de départ animation

        for i in range(n - 1):
            seg = canvas.create_line(
                idx_to_x(i), base_y, idx_to_x(i + 1), base_y,
                fill=TC, width=2, capstyle=tk.ROUND
            )
            seg_ids.append(seg)

        for i in range(n):
            dot = canvas.create_oval(
                idx_to_x(i) - 4, base_y - 4,
                idx_to_x(i) + 4, base_y + 4,
                fill=TC, outline='#000000', width=1
            )
            dot_ids.append(dot)
            vid = canvas.create_text(
                idx_to_x(i), base_y - 14,
                text=f"{values[i]:.2f}",
                fill="#FFFFFF", font=label_font, anchor='s'
            )
            val_ids.append(vid)

        # ── Animation (easing exponentiel) ────────────────────────────────────
        DELAY_MS = 16
        EASE     = 0.08
        THR      = 0.3   # seuil en pixels

        current_ys = [float(base_y)] * n

        def animate():
            done = True
            for i in range(n):
                diff = target_ys[i] - current_ys[i]
                if abs(diff) < THR:
                    current_ys[i] = target_ys[i]
                else:
                    current_ys[i] += diff * EASE
                    done = False

                cx = idx_to_x(i)
                cy = current_ys[i]

                # Mise à jour du point
                canvas.coords(dot_ids[i], cx - 4, cy - 4, cx + 4, cy + 4)
                canvas.coords(val_ids[i], cx, cy - 14)

                # Mise à jour du segment vers le point suivant
                if i < n - 1:
                    canvas.coords(seg_ids[i],
                                  cx, cy,
                                  idx_to_x(i + 1), current_ys[i + 1])

            if not done:
                root.after(DELAY_MS, animate)

        root.after(200, animate)

        # ── Capture PNG transparent (PrintWindow) ─────────────────────────────
        def capture_transparent_png():
            root.update_idletasks()
            hwnd_dc = win32gui.GetWindowDC(hwnd)
            mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            bmp     = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfc_dc, WIN_W, WIN_H)
            save_dc.SelectObject(bmp)
            ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0x2)
            bmp_info = bmp.GetInfo()
            bmp_bits = bmp.GetBitmapBits(True)
            img = Image.frombuffer('RGB',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_bits, 'raw', 'BGRX', 0, 1).convert("RGBA")
            win32gui.DeleteObject(bmp.GetHandle())
            save_dc.DeleteDC(); mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            pixels = img.load()
            for py in range(img.height):
                for px in range(img.width):
                    r, g, b, a = pixels[px, py]
                    if r <= 15 and g <= 15 and b <= 15:
                        pixels[px, py] = (0, 0, 0, 0)
            return img

        def copy_to_clipboard(img):
            png_buf = io.BytesIO()
            img.save(png_buf, format="PNG")
            CF_PNG  = win32clipboard.RegisterClipboardFormat("PNG")
            dib_buf = io.BytesIO()
            bg = Image.new("RGB", img.size, (0, 0, 0))
            bg.paste(img, mask=img.split()[3])
            bg.save(dib_buf, format="BMP")
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(CF_PNG, png_buf.getvalue())
                win32clipboard.SetClipboardData(win32con.CF_DIB,
                                                dib_buf.getvalue()[14:])
            finally:
                win32clipboard.CloseClipboard()

        def on_ctrl_c(e=None):
            copy_to_clipboard(capture_transparent_png())

        def on_ctrl_x(e=None):
            copy_to_clipboard(capture_transparent_png())
            root.after(50, close_all)

        root.bind("<Control-c>",  on_ctrl_c)
        root.bind("<Control-x>",  on_ctrl_x)
        ghost.bind("<Control-c>", on_ctrl_c)
        ghost.bind("<Control-x>", on_ctrl_x)

        ghost.mainloop()

    threading.Thread(target=_run, daemon=True).start()

loadPrint()#c

def boxChart(title, data, title_x_axis, title_y_axis, x_pos=100, y_pos=100):
    """
    Diagramme de quartiles horizontal (boîtes à moustaches).
    Chaque catégorie = une ligne. Les boîtes s'étendent de gauche à droite.
    Les valeurs min, Q1, médiane, Q3, max sont affichées sur chaque ligne.
    Non-bloquant. Ctrl+C = PNG transparent, Ctrl+X = PNG + ferme.

    data = {label: [liste de valeurs numériques]}
    """

    def _run():

        # ── Statistiques ──────────────────────────────────────────────────────
        stats = {}
        for lbl, vals in data.items():
            s     = sorted(vals)
            n     = len(s)
            med   = statistics.median(s)
            lower = s[:n // 2]
            upper = s[n // 2 + (n % 2):]
            q1    = statistics.median(lower) if lower else s[0]
            q3    = statistics.median(upper) if upper else s[-1]
            iqr   = q3 - q1
            w_low  = max(s[0],  q1 - 1.5 * iqr)
            w_high = min(s[-1], q3 + 1.5 * iqr)
            outliers = [v for v in s if v < w_low or v > w_high]
            stats[lbl] = (w_low, q1, med, q3, w_high, outliers)

        all_vals   = [v for lst in data.values() for v in lst]
        global_min = min(all_vals)
        global_max = max(all_vals)

        # ── Mesure polices ────────────────────────────────────────────────────
        _tmp = tk.Tk()
        _tmp.withdraw()
        _lf  = font.Font(family='Helvetica', size=10)
        _sf  = font.Font(family='Helvetica', size=8)
        _tf  = font.Font(family='Helvetica', size=14, weight='bold')

        max_label_w = max(_lf.measure(str(k)) for k in data.keys())
        title_w     = _tf.measure(title)

        val_range_raw = global_max - global_min if global_max != global_min else abs(global_max)
        raw_right = global_max + val_range_raw * 0.08
        raw_left  = global_min - val_range_raw * 0.08
        x_max     = (int(raw_right * 2) + 1) / 2.0
        x_min     = (int(raw_left  * 2))     / 2.0
        x_range   = x_max - x_min

        # Largeur des graduations X (sous l'axe)
        grad_w = max(_lf.measure(f"{x_min + i * x_range / 5:.2f}") for i in range(6))

        # Largeur des valeurs affichées sur les lignes (ex: "123.45")
        sample_val_w = _sf.measure(f"{global_max:.2f}")
        _tmp.destroy()

        TITLE_BAR_H   = 24
        # Marge gauche : assez pour les labels de catégorie
        MARGIN_LEFT   = int(max_label_w) + 20
        # Marge droite : assez pour afficher la valeur max (w_high) sans coupure
        MARGIN_RIGHT  = int(sample_val_w) + 16
        MARGIN_TOP    = 50 + TITLE_BAR_H
        # Marge bas : pour les graduations X et leur titre
        MARGIN_BOTTOM = 55

        # Hauteur par boîte
        BOX_SLOT = 60
        chart_h  = BOX_SLOT * len(data)

        WIN_H = MARGIN_TOP + chart_h + MARGIN_BOTTOM
        WIN_W = max(600, int(title_w) + 80,
                    MARGIN_LEFT + int(grad_w) * 6 + MARGIN_RIGHT)

        # ── Fenêtre fantôme ───────────────────────────────────────────────────
        ghost = tk.Tk()
        ghost.title(title)
        ghost.geometry("1x1+-32000+-32000")
        ghost.resizable(False, False)
        ghost.attributes('-alpha', 0.01)
        ghost.configure(bg='black')

        root = tk.Toplevel(ghost)
        root.title(title)
        root.geometry(f"{WIN_W}x{WIN_H}+{x_pos}+{y_pos}")
        root.configure(bg='black')
        root.overrideredirect(True)
        root.transient(ghost)

        # ── Drag ──────────────────────────────────────────────────────────────
        drag_state = {"x": 0, "y": 0, "dragging": False}

        def on_drag_start(e):
            drag_state["x"] = e.x_root; drag_state["y"] = e.y_root
            drag_state["dragging"] = True

        def on_drag_motion(e):
            if not drag_state["dragging"]: return
            dx = e.x_root - drag_state["x"]; dy = e.y_root - drag_state["y"]
            drag_state["x"] = e.x_root;      drag_state["y"] = e.y_root
            root.geometry(f"+{root.winfo_x()+dx}+{root.winfo_y()+dy}")

        def on_drag_stop(e): drag_state["dragging"] = False

        # ── Win32 ─────────────────────────────────────────────────────────────
        root.update_idletasks()
        hwnd = root.winfo_id(); ghost_hwnd = ghost.winfo_id()

        if sys.platform.startswith('win'):
            sx = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            sx = (sx | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW) \
                 & ~win32con.WS_EX_APPWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, sx)
            win32gui.SetLayeredWindowAttributes(
                hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)
            gx = win32gui.GetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE)
            gx = (gx | win32con.WS_EX_APPWINDOW) & ~win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(ghost_hwnd, win32con.GWL_EXSTYLE, gx)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_HIDE)
            win32gui.ShowWindow(ghost_hwnd, win32con.SW_SHOW)

        def bring_to_front(e=None):
            try:
                root.lift(); root.focus_force()
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            except Exception: pass

        ghost.bind("<Map>",     bring_to_front)
        ghost.bind("<FocusIn>", bring_to_front)

        def close_all():
            root.destroy(); ghost.destroy()

        # ── Canvas ────────────────────────────────────────────────────────────
        canvas = tk.Canvas(root, width=WIN_W, height=WIN_H,
                           bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        # Barre titre
        tb  = canvas.create_rectangle(0, 0, WIN_W, TITLE_BAR_H,
                                      fill='#1a1a1a', outline='#333333', width=1)
        tbl = canvas.create_text(WIN_W/2, TITLE_BAR_H/2, text=title,
                                 fill="#AAAAAA",
                                 font=font.Font(family='Helvetica', size=9))
        for item in (tb, tbl):
            canvas.tag_bind(item, "<ButtonPress-1>",  on_drag_start)
            canvas.tag_bind(item, "<B1-Motion>",       on_drag_motion)
            canvas.tag_bind(item, "<ButtonRelease-1>", on_drag_stop)

        # Bouton X
        CS = 18; CX_btn = WIN_W - CS - 4; CY_btn = 3
        cb = canvas.create_rectangle(CX_btn, CY_btn, CX_btn+CS, CY_btn+CS,
                                     fill='#cc3333', outline='', width=0)
        canvas.create_text(CX_btn+CS/2, CY_btn+CS/2, text="X", fill="white",
                           font=font.Font(family='Helvetica', size=9, weight='bold'))

        def on_click(e):
            if CX_btn <= e.x <= CX_btn+CS and CY_btn <= e.y <= CY_btn+CS:
                close_all()

        def on_hover(e):
            inside = CX_btn <= e.x <= CX_btn+CS and CY_btn <= e.y <= CY_btn+CS
            canvas.itemconfig(cb, fill='#ff5555' if inside else '#cc3333')

        canvas.bind("<ButtonPress-1>", on_click)
        canvas.bind("<Motion>",        on_hover)

        # ── Polices ───────────────────────────────────────────────────────────
        title_font = font.Font(family='Helvetica', size=14, weight='bold')
        label_font = font.Font(family='Helvetica', size=10)
        small_font = font.Font(family='Helvetica', size=8)

        chart_width  = WIN_W - MARGIN_LEFT - MARGIN_RIGHT
        chart_height = WIN_H - MARGIN_TOP  - MARGIN_BOTTOM

        # ── Axes ──────────────────────────────────────────────────────────────
        # Axe X (horizontal, en bas)
        canvas.create_line(MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           WIN_W - MARGIN_RIGHT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)
        # Axe Y (vertical, à gauche)
        canvas.create_line(MARGIN_LEFT, MARGIN_TOP,
                           MARGIN_LEFT, WIN_H - MARGIN_BOTTOM,
                           fill="#FFFFFF", width=2)

        # Titre principal
        chart_title_y = TITLE_BAR_H + (MARGIN_TOP - TITLE_BAR_H) / 2
        canvas.create_text(WIN_W/2, chart_title_y,
                           text=title, fill="#FFFFFF", font=title_font)

        # Titre axe X (bas)
        canvas.create_text(WIN_W/2, WIN_H - 12,
                           text=title_x_axis, fill="#FFFFFF", font=label_font)

        # Titre axe Y (gauche, vertical) — ici c'est les catégories
        canvas.create_text(12, WIN_H/2,
                           text=title_y_axis, fill="#FFFFFF",
                           font=label_font, angle=90)

        # Graduations X + grille verticale
        def val_to_x(v):
            return MARGIN_LEFT + (v - x_min) / x_range * chart_width

        x_step = x_range / 5
        for i in range(6):
            xv = x_min + i * x_step
            xp = val_to_x(xv)
            canvas.create_line(xp, WIN_H - MARGIN_BOTTOM,
                               xp, WIN_H - MARGIN_BOTTOM + 5,
                               fill="#FFFFFF", width=1)
            canvas.create_text(xp, WIN_H - MARGIN_BOTTOM + 14,
                               text=f"{xv:.2f}", fill="#FFFFFF",
                               font=small_font, anchor='n')
            if i > 0:
                canvas.create_line(xp, MARGIN_TOP, xp, WIN_H - MARGIN_BOTTOM,
                                   fill="#333333", width=1, dash=(4, 6))

        # ── Couleurs thème ────────────────────────────────────────────────────
        TC      = '#{:02x}{:02x}{:02x}'.format(*THEME_COLOR)
        TC_DARK = '#{:02x}{:02x}{:02x}'.format(
            int(THEME_COLOR[0]*0.4), int(THEME_COLOR[1]*0.4), int(THEME_COLOR[2]*0.4))
        TC_MED  = '#{:02x}{:02x}{:02x}'.format(
            int(THEME_COLOR[0]*0.12), int(THEME_COLOR[1]*0.12), int(THEME_COLOR[2]*0.12))

        # ── Construction des boîtes horizontales ──────────────────────────────
        labels_list = list(stats.keys())
        BOX_H       = BOX_SLOT * 0.40   # hauteur visuelle de la boîte
        WHISKER_H   = BOX_SLOT * 0.18   # hauteur des capuchons

        boxes = []

        for i, lbl in enumerate(labels_list):
            w_low, q1, med, q3, w_high, outliers = stats[lbl]
            cy = MARGIN_TOP + BOX_SLOT * (i + 0.5)   # centre Y de la boîte

            # Positions X cibles
            tx_wlow  = val_to_x(w_low)
            tx_q1    = val_to_x(q1)
            tx_med   = val_to_x(med)
            tx_q3    = val_to_x(q3)
            tx_whigh = val_to_x(w_high)
            tx_med0  = val_to_x(med)   # point de départ animation

            # Label de catégorie (axe Y gauche)
            canvas.create_text(MARGIN_LEFT - 10, cy,
                               text=lbl, fill="#FFFFFF",
                               font=label_font, anchor='e')

            # Ligne de séparation horizontale légère entre boîtes
            if i > 0:
                canvas.create_line(MARGIN_LEFT, cy - BOX_SLOT/2,
                                   WIN_W - MARGIN_RIGHT, cy - BOX_SLOT/2,
                                   fill="#222222", width=1)

            # ── Éléments graphiques (tous partent de la médiane) ───────────
            box_rect   = canvas.create_rectangle(
                tx_med0, cy - BOX_H/2, tx_med0, cy + BOX_H/2,
                fill=TC_MED, outline=TC, width=2)

            med_line   = canvas.create_line(
                tx_med0, cy - BOX_H/2, tx_med0, cy + BOX_H/2,
                fill=TC, width=2)

            whisk_low  = canvas.create_line(
                tx_med0, cy, tx_med0, cy,
                fill=TC_DARK, width=1, dash=(4, 3))

            whisk_high = canvas.create_line(
                tx_med0, cy, tx_med0, cy,
                fill=TC_DARK, width=1, dash=(4, 3))

            cap_low    = canvas.create_line(
                tx_med0, cy - WHISKER_H/2, tx_med0, cy + WHISKER_H/2,
                fill=TC, width=2)

            cap_high   = canvas.create_line(
                tx_med0, cy - WHISKER_H/2, tx_med0, cy + WHISKER_H/2,
                fill=TC, width=2)

            # ── Labels de valeur sur chaque ligne ─────────────────────────
            # Positionnés au-dessus de la boîte, alignés sur leur ligne respective
            LY = cy - BOX_H/2 - 5   # Y des labels (au-dessus de la boîte)

            lbl_wlow  = canvas.create_text(tx_med0, LY, anchor='s',
                text=f"{w_low:.2f}",  fill="#AAAAAA", font=small_font)
            lbl_q1    = canvas.create_text(tx_med0, LY, anchor='s',
                text=f"{q1:.2f}",    fill=TC,        font=small_font)
            lbl_med   = canvas.create_text(tx_med,  LY, anchor='s',
                text=f"{med:.2f}",   fill=TC,        font=small_font)
            lbl_q3    = canvas.create_text(tx_med0, LY, anchor='s',
                text=f"{q3:.2f}",    fill=TC,        font=small_font)
            lbl_whigh = canvas.create_text(tx_med0, LY, anchor='s',
                text=f"{w_high:.2f}", fill="#AAAAAA", font=small_font)

            # Outliers
            out_ids = []
            for ov in outliers:
                ox  = val_to_x(ov)
                oid = canvas.create_oval(ox-3, cy-3, ox+3, cy+3,
                                         fill='', outline=TC, width=1)
                out_ids.append(oid)

            boxes.append({
                'cy': cy, 'LY': LY,
                'box_rect': box_rect, 'med_line': med_line,
                'whisk_low': whisk_low, 'whisk_high': whisk_high,
                'cap_low': cap_low, 'cap_high': cap_high,
                'lbl_wlow': lbl_wlow, 'lbl_q1': lbl_q1, 'lbl_med': lbl_med,
                'lbl_q3': lbl_q3, 'lbl_whigh': lbl_whigh,
                'out_ids': out_ids,
                # cibles
                'tx_wlow': tx_wlow, 'tx_q1': tx_q1,
                'tx_q3':   tx_q3,   'tx_whigh': tx_whigh,
                'tx_med':  tx_med,
                # courants (animation depuis la médiane)
                'cx_wlow': tx_med0, 'cx_q1': tx_med0,
                'cx_q3':   tx_med0, 'cx_whigh': tx_med0,
            })

        # ── Animation ─────────────────────────────────────────────────────────
        DELAY_MS = 16
        EASE     = 0.08
        THR      = 0.3

        def animate():
            done = True
            for b in boxes:
                cy  = b['cy']
                LY  = b['LY']
                bh  = BOX_H / 2
                wh  = WHISKER_H / 2

                for key_cur, key_tgt in (
                    ('cx_q1',    'tx_q1'),
                    ('cx_q3',    'tx_q3'),
                    ('cx_wlow',  'tx_wlow'),
                    ('cx_whigh', 'tx_whigh'),
                ):
                    diff = b[key_tgt] - b[key_cur]
                    if abs(diff) < THR:
                        b[key_cur] = b[key_tgt]
                    else:
                        b[key_cur] += diff * EASE
                        done = False

                cq1 = b['cx_q1'];  cq3 = b['cx_q3']
                cwl = b['cx_wlow']; cwh = b['cx_whigh']
                cmd = b['tx_med']   # médiane : fixe

                canvas.coords(b['box_rect'],   cq1, cy-bh,  cq3, cy+bh)
                canvas.coords(b['med_line'],   cmd, cy-bh,  cmd, cy+bh)
                canvas.coords(b['whisk_low'],  cwl, cy,     cq1, cy)
                canvas.coords(b['whisk_high'], cq3, cy,     cwh, cy)
                canvas.coords(b['cap_low'],    cwl, cy-wh,  cwl, cy+wh)
                canvas.coords(b['cap_high'],   cwh, cy-wh,  cwh, cy+wh)

                # Mise à jour positions labels
                canvas.coords(b['lbl_wlow'],  cwl, LY)
                canvas.coords(b['lbl_q1'],    cq1, LY)
                canvas.coords(b['lbl_q3'],    cq3, LY)
                canvas.coords(b['lbl_whigh'], cwh, LY)
                # lbl_med est fixe, déjà positionné

            if not done:
                root.after(DELAY_MS, animate)

        root.after(200, animate)

        # ── Capture & clipboard ───────────────────────────────────────────────
        def capture_transparent_png():
            root.update_idletasks()
            hwnd_dc = win32gui.GetWindowDC(hwnd)
            mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            bmp     = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfc_dc, WIN_W, WIN_H)
            save_dc.SelectObject(bmp)
            ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0x2)
            bmp_info = bmp.GetInfo(); bmp_bits = bmp.GetBitmapBits(True)
            img = Image.frombuffer('RGB',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_bits, 'raw', 'BGRX', 0, 1).convert("RGBA")
            win32gui.DeleteObject(bmp.GetHandle())
            save_dc.DeleteDC(); mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            pixels = img.load()
            for py in range(img.height):
                for px in range(img.width):
                    r, g, b, a = pixels[px, py]
                    if r <= 15 and g <= 15 and b <= 15:
                        pixels[px, py] = (0, 0, 0, 0)
            return img

        def copy_to_clipboard(img):
            png_buf = io.BytesIO(); img.save(png_buf, format="PNG")
            CF_PNG  = win32clipboard.RegisterClipboardFormat("PNG")
            dib_buf = io.BytesIO()
            bg = Image.new("RGB", img.size, (0, 0, 0))
            bg.paste(img, mask=img.split()[3]); bg.save(dib_buf, format="BMP")
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(CF_PNG, png_buf.getvalue())
                win32clipboard.SetClipboardData(win32con.CF_DIB, dib_buf.getvalue()[14:])
            finally:
                win32clipboard.CloseClipboard()

        def on_ctrl_c(e=None): copy_to_clipboard(capture_transparent_png())
        def on_ctrl_x(e=None):
            copy_to_clipboard(capture_transparent_png())
            root.after(50, close_all)

        root.bind("<Control-c>",  on_ctrl_c)
        root.bind("<Control-x>",  on_ctrl_x)
        ghost.bind("<Control-c>", on_ctrl_c)
        ghost.bind("<Control-x>", on_ctrl_x)

        ghost.mainloop()

    threading.Thread(target=_run, daemon=True).start()

loadPrint()#c

def createChart( chart: str, title: str, data: dict, x_axis_title: str, y_axis_title: str ):
    try:
        if chart == "bandChart":
            bandChart( title, data, x_axis_title, y_axis_title )
        elif chart == "pieChart":
            pieChart( title, data )
        elif chart == "lineChart":
            lineChart( title, data, x_axis_title, y_axis_title )
        elif chart == "boxChart":
            boxChart( title, data, x_axis_title, y_axis_title )
        else:
            return f"Auncun diagramme disponible sous le nom de {chart}", True
        return f"Diagramme {chart} créé", False
    except Exception as e:
        log( "Error while creating chart", {"error": str( e ), "data": data, "type": chart}, "error" )
        return f"Erreur lors de la création du diagramme : {str( e )}", True

loadPrint()#c

def widget( prompt, script: str = "script.py" ):
    config = f"""
Tu es un expert Python qui génère des widgets graphiques avec tkinter sur Windows 11 (Python 3.12).

## Mécanisme de transparence — CRITIQUE

Le colorkey fonctionne ainsi : tout pixel RGB(0,0,0) exact = invisible à l'écran.
Le fond de la fenêtre EST noir (0,0,0) — il sera donc transparent visuellement.
Les éléments UI (barre, boutons, texte) sont dessinés par-dessus en couleurs non-noires.

### Règles absolues :
- root.config(bg='black') — le fond DOIT être noir pur
- Les éléments UI utilisent des couleurs NON-noires (jamais #000000 / (0,0,0) / 'black' sur un élément visible)
- Si du noir est nécessaire dans le design, utiliser #010101
- Le fond apparaîtra transparent à l'écran grâce au colorkey — c'est le comportement voulu

### tkinter (ordre STRICT) :
1. root.config(bg='black')
2. root.overrideredirect(True)
3. Tous les Frame/Canvas enfants avec bg NON-noir
4. root.wm_attributes('-transparentcolor', 'black')
5. root.update()
6. bloc win32 (voir ci-dessous)

### Initialisation win32 (après root.update()) :
hwnd = int(root.wm_frame(), 16)

win32gui.SetWindowLong(
    hwnd, win32con.GWL_EXSTYLE,
    (win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED) & ~win32con.WS_EX_APPWINDOW
)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

## Règles du widget

- Couleur thème : RGB{THEME_COLOR}
- Le fond (corps) du widget est noir (0,0,0) — transparent grâce au colorkey
- Positionné dans un coin supérieur de l'écran (y > 0, x > 0, jamais à 0)
- Interface entièrement en français
- Déplaçable via une barre de titre en haut du widget
- Bouton X sur la barre de titre pour fermer le widget
- Animation d'entrée au lancement
- Widget toujours au premier plan (HWND_TOPMOST)
- Lever raise SystemExit("script closed normally by user") à la fermeture avec le bouton X
- Ajoute le plus d'informations utiles possibles dans le widget, tant qu'elles sont en rapport avec le but du widget

## Qualité du code

- Vérifier l'absence d'erreurs avant de retourner le script
- S'assurer que le déplacement, la fermeture et le z-order (topmost) fonctionnent correctement
- Aucune clé API requise

## Format de sortie — TOUJOURS retourner ce JSON exact, sans balises ```, tel quel :

{"{"}
    "message": "Réponse à l'utilisateur",
    "script": "Le script Python complet",
    "dependencies": ["nom_dep_1", "nom_dep_2"]
{"}"}

Règles du JSON :
- "dependencies" : noms bruts uniquement (ex: "pywin32"), pas de commandes pip
- Pas de markdown autour du JSON, pas de ```, retourner le JSON brut directement
"""

    sub_conversation = [
        {
            "role": "system",
            "content": config
        }
    ]

    # prompt = """
    # Le niveau de la batterie et les performances de l'ordi
    # """

    sub_conversation.append(
        {
            "role": "user",
            "content": "Fait moi ceci avec un fond transparent :\n" + prompt + "\nAssure toi que le widget soit interactif pour répondre aux demandes des configurations"
        }
    )
    try:
        while True:
            # raw_response = Model.askModel( CODE_MODEL, sub_conversation, "high", MAX_RETRIES, Model.Verification.isJson )
            raw_response = Model.askModel( sub_conversation, Model.Verification.isJson )
            
            # if raw_response == "":
            #     print( "ai finished task, exiting..." )
            #     raise FunctionEnd( "End of function" )
            log( "Widget creation", f"model raw response : {raw_response}", "info" )
            try:
                response = json.loads( raw_response )
                try:
                    if response["script-finished"]:
                        raise FunctionEnd( "End of function" )
                except KeyError:
                    pass


                # print( json.dumps( response, indent=4 ) )
                log( "Widget creation", {"message": "model formatted response", "response": response}, "info" )

                sub_conversation.append(
                    {
                        "role": "assistant",
                        "content": raw_response
                    }
                )
                # print( response["message"] )
                with open( script, "w", encoding="utf-8" ) as f:
                    f.write( "# -*- coding: utf-8 -*-\n" )
                    f.write( response["script"] )

                try:
                    _ = response["depedencies"]
                    # print( "installing" )
                    for dependecie in response["depedencies"]:
                        command = f"pip3 install {dependecie}"
                        print( f"Installing : {command}" )
                        os.system( command )
                except KeyError:
                    pass

                # print( "executing" )
                try:
                    result = subprocess.run( ["python3", f"./{script}"], capture_output=True, text=True, check=True )
                    # Vérifier aussi s'il y a des erreurs dans stderr même si l'exécution a réussi
                    if result.stderr:
                        prompt = f"Avertissements ou erreurs lors de l'exécution:\n{result.stderr}\nSortie du programme:\n{result.stdout}"
                        if result.stderr.lower().find( "script closed normally by user" ) != -1:
                            raise FunctionEnd( "End of function" )
                        log( "Error for widget execution", {"error": result.stderr, "out": result.stdout}, "warning" )
                        # print( result.stderr )
                    else:
                        raise FunctionEnd( "End of function" )
                except subprocess.CalledProcessError as e:
                    prompt = f"Erreur lors de l'exécution du script (code {e.returncode}):\n{e.stderr}"
                    # print( e.stderr )
                    log( "Error for widget execution", {"error": str( e ), "info": e.stderr}, "warning" )
                    if e.stderr.lower().find( "script closed normally by user" ) != -1:
                        raise FunctionEnd( "End of function" )
                except Exception as e:
                    prompt = f"Erreur lors de l'exécution du script (code {e.returncode}):\n{e.stderr}"
                    # print( e )
                    log( "Error for widget execution", {"error": str( e ), "info": e.stderr}, "warning" )
                    if e.stderr.lower().find( "script closed normally by user" ) != -1:
                        raise FunctionEnd( "End of function" )
                
                sub_conversation.append(
                    {
                        "role": "user",
                        "content": prompt
                    }
                )
                # Json.write( sub_conversation, "a.json" )
                log( "Widget sub_conversation", sub_conversation, "info" )
            except json.JSONDecodeError:
                pass
            except KeyError:
                pass
    except FunctionEnd:
        return
    except KeyboardInterrupt:
        Json.write( sub_conversation, f"{DEBUG_PATH}conversation-debug-widget-{script}.json" )
    except NoResponseError as e:
        Json.write( sub_conversation, f"{DEBUG_PATH}conversation-debug-widget-{script}.json" )

loadPrint()#c

def createWidget( description ):
    sendNotification( "Widget créé" )
    widget_thread = threading.Thread( target=widget, args=( description, f"{CACHE_PATH}{time.time()}.py" ) )
    widget_thread.start()
    return "Widget affiché avec succès", False

loadPrint()#c

def _record_single(p: pyaudiowpatch.PyAudio, device_index: int, sample_rate: int,
                   channels: int, duration: int) -> np.ndarray | None:
    """Enregistre depuis un device via callback (non-bloquant)."""
    frames         = []
    num_chunks     = int(sample_rate / 1024 * duration)
    done_event     = threading.Event()

    try:
        stream = p.open(
            format=pyaudiowpatch.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=1024,
            stream_callback=_record_stream_callback(frames, num_chunks, done_event),
        )
        stream.start_stream()
        done_event.wait(timeout=TIMEOUT)
        stream.stop_stream()
        stream.close()
    except Exception as e:
        return None

    if not frames:
        return None

    raw   = b"".join(frames)
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    if channels == 2:
        audio = audio.reshape(-1, 2).mean(axis=1)

    if sample_rate != SAMPLE_RATE:
        try:
            from scipy.signal import resample_poly
            from math import gcd
            g     = gcd(SAMPLE_RATE, sample_rate)
            audio = resample_poly(audio, SAMPLE_RATE // g, sample_rate // g)
        except ImportError:
            new_len = int(len(audio) * SAMPLE_RATE / sample_rate)
            audio   = np.interp(
                np.linspace(0, len(audio) - 1, new_len),
                np.arange(len(audio)),
                audio,
            )

    return audio

loadPrint()#c

def _record_both_parallel(loopback_device: dict | None) -> tuple[np.ndarray | None, np.ndarray | None]:
    """
    Enregistre speaker et micro en parallèle via callbacks dans une seule
    instance PyAudio — évite le crash natif lié à 2 instances simultanées.
    """
    # ── Paramètres speaker ────────────────────────────────────────────────────
    speaker_params = None
    if loopback_device:
        speaker_params = (
            int(loopback_device["index"]),
            int(loopback_device["defaultSampleRate"]),
            min(int(loopback_device["maxInputChannels"]), 2),
        )

    # ── Paramètres micro ──────────────────────────────────────────────────────
    mic_params = None
    p_tmp = pyaudiowpatch.PyAudio()
    try:
        dev_info   = p_tmp.get_default_input_device_info()
        mic_params = (
            int(dev_info["index"]),
            int(dev_info["defaultSampleRate"]),
            1,
        )
    except Exception:
        pass
    finally:
        p_tmp.terminate()

    # ── Une seule instance PyAudio pour les deux streams ──────────────────────
    p = pyaudiowpatch.PyAudio()

    speaker_frames     = []
    mic_frames         = []
    speaker_done       = threading.Event()
    mic_done           = threading.Event()
    speaker_stream     = None
    mic_stream         = None

    try:
        if speaker_params:
            s_idx, s_rate, s_ch = speaker_params
            s_chunks = int(s_rate / 1024 * DURATION)
            speaker_stream = p.open(
                format=pyaudiowpatch.paInt16,
                channels=s_ch,
                rate=s_rate,
                input=True,
                input_device_index=s_idx,
                frames_per_buffer=1024,
                stream_callback=_record_stream_callback(speaker_frames, s_chunks, speaker_done),
            )
            speaker_stream.start_stream()

        if mic_params:
            m_idx, m_rate, m_ch = mic_params
            m_chunks = int(m_rate / 1024 * DURATION)
            mic_stream = p.open(
                format=pyaudiowpatch.paInt16,
                channels=m_ch,
                rate=m_rate,
                input=True,
                input_device_index=m_idx,
                frames_per_buffer=1024,
                stream_callback=_record_stream_callback(mic_frames, m_chunks, mic_done),
            )
            mic_stream.start_stream()

        # Attend que les deux aient fini (ou timeout)
        if speaker_params:
            speaker_done.wait(timeout=TIMEOUT)
        if mic_params:
            mic_done.wait(timeout=TIMEOUT)

    finally:
        for stream in (speaker_stream, mic_stream):
            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception:
                    pass
        p.terminate()

    # ── Post-traitement ───────────────────────────────────────────────────────
    def process(frames: list, sample_rate: int, channels: int) -> np.ndarray | None:
        if not frames:
            return None
        raw   = b"".join(frames)
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if channels == 2:
            audio = audio.reshape(-1, 2).mean(axis=1)
        if sample_rate != SAMPLE_RATE:
            try:
                from scipy.signal import resample_poly
                from math import gcd
                g     = gcd(SAMPLE_RATE, sample_rate)
                audio = resample_poly(audio, SAMPLE_RATE // g, sample_rate // g)
            except ImportError:
                new_len = int(len(audio) * SAMPLE_RATE / sample_rate)
                audio   = np.interp(
                    np.linspace(0, len(audio) - 1, new_len),
                    np.arange(len(audio)),
                    audio,
                )
        return audio

    speaker_audio = process(speaker_frames, *speaker_params[1:]) if speaker_params else None
    mic_audio     = process(mic_frames,     *mic_params[1:])     if mic_params     else None

    if mic_audio is not None:
        mic_audio = np.clip(mic_audio * MIC_GAIN, -1.0, 1.0)

    if speaker_audio is not None:
        sf.write("recording_speaker.wav", speaker_audio, SAMPLE_RATE)

    if mic_audio is not None:
        sf.write("recording_mic.wav", mic_audio, SAMPLE_RATE)

    return speaker_audio, mic_audio

loadPrint()#c

async def identify(audio: np.ndarray, label: str = "") -> dict | None:
    shazam    = Shazam()
    sf.write(f"debug_{label}.wav", audio, SAMPLE_RATE)

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
    track    = result.get("track", {})
    name     = track.get("title",    "Inconnu")
    artist   = track.get("subtitle", "Inconnu")
    sections = track.get("sections", [])

    album = "Inconnu"
    for section in sections:
        for meta in section.get("metadata", []):
            if meta.get("title", "").lower() == "album":
                album = meta.get("text", "Inconnu")

    genre       = track.get("genres", {}).get("primary", "Inconnu")
    publication = "Inconnu"
    for section in sections:
        for meta in section.get("metadata", []):
            if meta.get("title", "").lower() in ("released", "year", "année", "date de sortie"):
                publication = meta.get("text", "Inconnu")

    return {
        "name":        name,
        "artist":      artist,
        "album":       album,
        "genre":       genre,
        "publication": publication,
    }

loadPrint()#c

async def _recognize_music_async() -> dict:
    p               = pyaudiowpatch.PyAudio()
    loopback_device = get_default_wasapi_loopback_device(p)
    p.terminate()

    speaker_audio, mic_audio = _record_both_parallel(loopback_device)

    async def identify_speaker() -> dict | None:
        if speaker_audio is not None and rms(speaker_audio) > SPEAKER_SILENCE_THRESH:
            result = await identify(speaker_audio, "speaker")
            if result:
                return extract_track_info(result)
        return None

    async def identify_mic() -> dict | None:
        if mic_audio is not None and rms(mic_audio) > MIC_SILENCE_THRESH:
            result = await identify(mic_audio, "micro")
            if result:
                return extract_track_info(result)
        return None

    speaker_info, mic_info = await asyncio.gather(
        identify_speaker(),
        identify_mic(),
    )

    return {
        "speaker":    speaker_info,
        "microphone": mic_info,
    }

loadPrint()#c

def recognizeMusic() -> dict:
    """Point d'entrée public. Retourne un dict avec les infos de la musique détectée."""
    data = asyncio.run(_recognize_music_async())
    spotify_data = spotify.nowPlaying()
    speaker_data = data["speaker"]
    microphone_data = data["microphone"]
    to_return =  "Aucune chanson trouvé"
    if microphone_data != None:
        to_return = "Chanson trouvé sur le microphone :\n" + str( microphone_data )
    if speaker_data != None:
        to_return = "Chanson trouvé sur le microphone :\n" + str( speaker_data )
    if spotify_data != None:
        to_return = "Chanson trouvé sur le microphone :\n" + str( spotify_data )
    print( to_return )
    return to_return, True

loadPrint()#c

def setMusicState( state: bool ):
    global spotify

    if not IS_THERE_SPOTIFY:
        log( "Playing spotify error", "No spotify, Impossible de faire jouer de la musique", "error" )
        return "Impossible de faire jouer de la musique", True
    
    while True:
        devices = spotify.listDevices()
        # print( f"{devices=}" )
        log( "Spotify devices", devices, "info" )
        if devices == []:
            spotify.openSpotify()
        else:
            break


    if state:
        spotify.resume()
        return "La chanson a bien été repartie", False
    else:
        spotify.pause()
        return "La chanson a bien été pausé", False

loadPrint()#c

def changeMusicTrack( target: str ):
    global spotify

    if not IS_THERE_SPOTIFY:
        log( "Playing spotify error", "No spotify, Impossible de faire jouer de la musique", "error" )
        return "Impossible de faire jouer de la musique", True
    
    while True:
        devices = spotify.listDevices()
        # print( f"{devices=}" )
        log( "Spotify devices", devices, "info" )
        if devices == []:
            spotify.openSpotify()
        else:
            break

    if target == "next":
        spotify.nextTrack()
        return "La prochaine musique joue maintenant", False
    elif target == "previous":
        spotify.previousTrack()
        return "La musique précédente joue maintenant", False
    else:
        return f"Le choix \"{target}\" n'est pas valide, acceptés : \"next\" ou \"previous\"", True

loadPrint()#c

def playMusic( search, types, choosed_device, volume ):
    devices = spotify.listDevices()
    if not IS_THERE_SPOTIFY:
        log( "Playing spotify error", "No spotify, Impossible de faire jouer de la musique", "error" )
        return "Impossible de faire jouer de la musique", True
    try:
        while True:
            devices = spotify.listDevices()
            # print( f"{devices=}" )
            log( "Spotify devices", devices, "info" )
            if devices == []:
                spotify.openSpotify()
            else:
                break
        found = False
        for device in devices:
            if device["type"] == choosed_device:
                found = True
                device_id = device["id"]
        if not found:
            return "Appareil impossible à trouver. Assurez vous que l'application est ouverte sur l'appareil en question", True
        results, _ = spotify.search( search, types )
        spotify.play( results[0]["uri"], device_id )
        spotify.setVolume( volume, device_id )
        return "Succès pour faire jouer le titre", False
    except Exception as e:
        log( "Spotify error", str( e ), "error" )
        return "Erreur pour faire jouer le contenu", True
    # else:
    #     return "Type(s) non valide", True

loadPrint()#c

# =====================
# TOOL: openLink
# =====================
def openLink( query: str, is_direct_link ):
    if is_direct_link:
        success = webbrowser.open( query )
        if success:
            return f"ouverture de {query} réussie", False
        return f"ouverture de {query} raté", True
    
    for i in range( MAX_RETRIES ):
        try:
#             link = Model.askModel(
#                 WEB_MODEL,
#                 [
#                     {
#                         "role": "system",
#                         "content": """
# Ton role est de donner un lien web à entrer dans un navigateur.
# Tu dois uniquement donner le lien web et rien d'autre.
# Le lien que tu vas donner doit corresprondre le plus possible à la demande de l'utilisateur
# """
#                     },
#                     {
#                         "role": "user",
#                         "content": query
#                     }
#                 ],
#                 "high",
#                 MAX_RETRIES,
#                 Model.Verification.isLink
#             )
            # FIXME : Make ai search for real link, not just guess
            link = Model.askModel(
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
                Model.Verification.isLink
            )

            success = webbrowser.open( link )
            if success:
                return f"ouverture de {link} réussie", False
        except NoResponseError as e:
            pass
    return f"ouverture de {link} raté", True

loadPrint()#c

# =====================
# TOOL: openApp
# =====================
def launchApp( app ):
    log( "Launching app", f"app {json.dumps( app, indent=4 )}", "info" )
    try:
        subprocess.Popen( [app["path"]], creationflags=subprocess.DETACHED_PROCESS, shell=False)
    except PermissionError:
        log( "Lauching app", f"not enough authorization for app {json.dumps( app, indent=4 )}", "error" )
        return "Permission insuffisante pour lancer cette application", True
    return "Application lancé avec succès", False

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
        try:
#             path = Model.askModel(
#                 SIMPLE_MODEL,
#                 [
#                     {
#                         "role": "system",
#                         "content": f"""
# Voici une liste d'applications :
# {json.dumps(apps, indent=4, ensure_ascii=False)}
# L'utilisateur va te donner un nom d'application, et tu dois UNIQUEMENT ressortir le nom de l'application.
# Tu dois ressortir UNIQUEMENT le nom, rien d'autre.
# Le nom de l'application doit correspondre à un des noms dans la liste avec la clé "name".
# Les applications n'ont pas tout le temps le même nom, tu dois donc choisir l'application qui correspond le mieux à la demande de l'utilisateur, en te basant sur la liste d'applications que je t'ai donnée.
# Ne ressort RIEN D'AUTRE que le nom, absolument rien d'autre, pas ton raisonnement, par tes doutes, uniquement un nom valide pour l'exécution de l'application demandée par l'utilisateur.
# Si tu hésite entre plusieurs, donne uniquement UN nom entre ceux que tu hésites
#     """
#                     },
#                     {
#                         "role": "user",
#                         "content": app
#                     }
#                 ],
#                 "high",
#                 MAX_RETRIES,
#                 Model.Verification.rawResponse
#             )

            path = Model.askModel(
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
        except NoResponseError as e:
            pass
    return f"Impossible de trouver l'application {app}", True

loadPrint()#c

def openApp( app ):
    global get_all_apps_thread, APPLICATIONS
    print( f"searching for {app}..." )
    get_all_apps_thread.join()
    get_all_apps_thread = Substitute()
    APPLICATIONS = Json.read( f"{CACHE_PATH}applications.json" )
    search = searchApp( APPLICATIONS, app )
    APPLICATIONS = None
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
                with conversation_mutex:
                    conversation = [ conversation[0], conversation[1] ]
                    if SERVER_URL:
                        requests.post( f"{SERVER_URL}/{SET_CONVERSATION}", json=conversation )
                    Json.write( conversation, CONVERSATION_PATH )
                sendNotification( "Historique effacé pour alléger la conversation" )
            else:
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
        with conversation_mutex:
            json.dump( conversation, f, indent=4, ensure_ascii=False )
    if AUDIO:
        Sound.waitForSoundTofinish()
        Sound.generateVoice( text, VOICE )
        Sound.playVoice()
    doProtocol( settings["reset-protocol-name"] )


loadPrint()#c

def saveFile( name, content ):
    try:
        if os.path.exists( f"{os.path.expanduser("~")}/Downloads/{name}" ):
            return f"Le fichier {name} existe déjà", True
        file = open( f"{os.path.expanduser("~")}/Downloads/{name}", 'w' )
        file.write( content )
        file.close()
        subprocess.Popen( ["notepad", f"{os.path.expanduser("~")}/Downloads/{name}"], creationflags=subprocess.DETACHED_PROCESS, shell=True)
        # os.system( f"notepad {os.path.expanduser("~")}/Downloads/{name}" )
        return f"Le fichier {name} a bien été créé", False
    except Exception as e:
        log( "Error while creating file", str( e ), "error" )
        return "Erreur lors de la création du fichier", True

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


def moment_actuel() -> dict:
    """
    Retourne un dictionnaire avec toutes les informations sur le moment actuel.
    """
    def _moment_journee(heure: int) -> str:
        if 5 <= heure < 12:
            return "matin"
        elif 12 <= heure < 14:
            return "midi"
        elif 14 <= heure < 18:
            return "après-midi"
        elif 18 <= heure < 22:
            return "soirée"
        else:
            return "nuit"
    maintenant = datetime.datetime.now()

    return {
        "date": {
            "annee": maintenant.year,
            "mois": maintenant.month,
            "nom_mois": maintenant.strftime("%B"),
            "jour": maintenant.day,
            "nom_jour": maintenant.strftime("%A"),
            "jour_de_annee": maintenant.timetuple().tm_yday,
            "semaine_de_annee": maintenant.isocalendar()[1],
            "trimestre": (maintenant.month - 1) // 3 + 1,
        },
        "heure": {
            "heure": maintenant.hour,
            "minute": maintenant.minute,
            "seconde": maintenant.second,
            "microseconde": maintenant.microsecond,
            "periode": "AM" if maintenant.hour < 12 else "PM",
            "moment_journee": _moment_journee(maintenant.hour),
        },
        "formats": {
            "iso": maintenant.isoformat(),
            "date_seule": maintenant.strftime("%Y-%m-%d"),
            "heure_seule": maintenant.strftime("%H:%M:%S"),
            "lisible": maintenant.strftime("%A %d %B %Y à %H:%M:%S"),
            "timestamp_unix": maintenant.timestamp(),
        },
        "calendrier": {
            "est_weekend": maintenant.weekday() >= 5,
            "jours_dans_mois": calendar.monthrange(maintenant.year, maintenant.month)[1],
            "est_annee_bissextile": calendar.isleap(maintenant.year),
        },
    }

loadPrint()#c

class StopWatch:
    class ChronoNotStarted( Exception ):
        """Chrono not started"""
        pass

    class ChronoNotStopped( Exception ):
        """Chrono not stopped"""
        pass

    class TimerNotStarted( Exception ):
        """Timer not started"""
        pass

    def timestampToDict(total_seconds: float):
        if total_seconds < 0:
            return {"error": "La durée ne peut pas être négative."}
        
        if total_seconds == 0:
            return {
                "jours": 0, "heures": 0, "minutes": 0, "secondes": 0,
                "milliseconde": 0, "microseconde": 0, "duree_totale_secondes": 0.0
            }

        # 1. Détermination des unités fixes
        
        # Calcul des jours
        SECONDS_POUR_UN_JOUR = 24 * 60 * 60 # 86400
        jours = int(total_seconds // SECONDS_POUR_UN_JOUR)
        
        # Calcul des secondes restantes après déduction des jours
        seconds_restantes = total_seconds % SECONDS_POUR_UN_JOUR
        
        # Calcul des heures
        SECONDS_POUR_UNE_HEURE = 60 * 60 # 3600
        heures = int(seconds_restantes // SECONDS_POUR_UNE_HEURE)
        
        # Calcul des secondes restantes après déduction des heures
        seconds_restantes = seconds_restantes % SECONDS_POUR_UNE_HEURE
        
        # Calcul des minutes
        minutes = int(seconds_restantes // 60)
        
        # Calcul des secondes et du reste de la précision
        secondes = int(seconds_restantes % 60)
        
        # La précision (millisecondes/microsecondes) vient de la partie flottante
        # On utilise la soustraction pour obtenir la partie décimale totale
        duree_entiere_seconde = int(total_seconds)
        partie_flottante = total_seconds - duree_entiere_seconde
        
        microsecondes = int(partie_flottante * 1000000)
        milliseconde = int(round(microsecondes / 1000))
        
        
        resultat = {
            "duree_totale_secondes": round(total_seconds, 4),
            "jours": jours,
            "heures": heures,
            "minutes": minutes,
            "secondes": secondes,
            "milliseconde": milliseconde,
            "microseconde": microsecondes,
        }
        
        return resultat


    class chrono:
        start_time = -1
        stop_time = -1

        def start( self ):
            self.start_time = time.time()
        
        def stop( self ):
            if self.start_time == -1:
                raise StopWatch.ChronoNotStarted( "Chrono not started. Please start the chonometer before stopping it" )
            self.stop_time = time.time() 

        def getMesuredTime( self ):
            if self.start_time == -1:
                raise StopWatch.ChronoNotStarted( "Chrono not started. Please start the chonometer before mesuring its time" )
            if self.stop_time == -1:
                raise StopWatch.ChronoNotStopped( "Chrono not stopped. Please stop the chonometer before mesuring its time" )
            mesured = self.stop_time - self.start_time
            return StopWatch.timestampToDict( mesured )

        def resetChrono( self ):
            self.start_time = -1
            self.stop_time = -1
    
    class timer:
        duration = 0
        target = None
        args = ()
        thread = None
        start_time = -1
        def __init__( self, duration, finish_target, args = () ):
            self.duration = duration
            self.target = finish_target
            self.args = args
            
        def _cooldown( self ):
            time.sleep( self.duration )
            self.start_time = -1
            self.target(*self.args)
        
        def start( self ):
            self.thread = threading.Thread( target=self._cooldown, name="timer" )
            self.start_time = time.time()
            self.thread.start()
        
        def getRemainingTime( self ):
            if self.start_time == -1:
                raise StopWatch.TimerNotStarted( "Timer not started. Please start timer before getting remaining time" )
            difference = time.time() - self.start_time
            duration = StopWatch.timestampToDict( difference )["duree_totale_secondes"]
            if self.duration - duration < 0:
                return 0.0
            return self.duration - duration
        
        def waitTimer( self ):
            self.thread.join()

loadPrint()#c

timer = None
chrono = StopWatch.chrono()

loadPrint()#c

def whenTimerFinished( say, audio ):
    global conversation
    sendNotification( say )
    if audio:
        Sound.waitForSoundTofinish()
        Sound.generateVoice( say, VOICE )
        Sound.playVoice()
    with conversation_mutex:
        conversation.append(
            {
                "role": "user",
                "content": "Timer terminé",
                "name": "timerFinished"
            }
        )

loadPrint()#c

def startTimer( say, duration ):
    global timer, AUDIO
    timer = StopWatch.timer( duration, whenTimerFinished, ( say, AUDIO ) )
    timer.start()
    return f"Timer de {duration} secondes parti", False

loadPrint()#c

def getRemainingTimerTime():
    global timer
    try:
        return "Il reste " + str( timer.getRemainingTime() ) + "s au timer", True
    except StopWatch.TimerNotStarted:
        return "Le timer n'a pas été parti ou est terminé", True

loadPrint()#c

def startChrono():
    global chrono
    chrono.resetChrono()
    chrono.start()
    return "Chronomètre parti", False

loadPrint()#c

def getChrono():
    global chrono
    try:
        chrono.stop()
        return str( chrono.getMesuredTime() ) + 's', True
    except StopWatch.ChronoNotStarted:
        return "Le chronomètre n'est pas parti.", True

loadPrint()#c

def getTime():
    try:
        return moment_actuel(), True
    except Exception as e:
        log( "Error while getting time", str( e ), "error" )
        return "Error pour obtenir le temps présent", True
    
loadPrint()#c

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
            return {
                "method": "ip",
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
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
        except Exception as exc:
            return {"method": "ip", "error": str(exc)}

    def _get_windows() -> dict:
        try:
            import win32com.client
        except ImportError:
            return {"method": "windows",
                    "error": "pywin32 non installé (pip install pywin32)"}
        try:
            locator = win32com.client.Dispatch("Windows.Devices.Geolocation.Geolocator")

            access = locator.RequestAccessAsync()
            deadline = time.time() + 10
            while access.Status != 4 and time.time() < deadline:
                time.sleep(0.1)
            if access.Status == 4 and access.GetResults() != 0:
                return {"method": "windows", "error": "Accès à la localisation refusé"}

            locator.DesiredAccuracy = 0
            locator.DesiredAccuracyInMeters = 10

            op = locator.GetGeopositionAsync()
            deadline = time.time() + 30
            while op.Status != 4 and time.time() < deadline:
                time.sleep(0.2)
            if op.Status != 4:
                return {"method": "windows", "error": "Délai dépassé (30 s)"}

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

            return {
                "method": "windows",
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
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
        except Exception as exc:
            return {"method": "windows", "error": str(exc)}

    def _compare(ip: dict, win: dict) -> dict:
        if "error" in ip or "error" in win:
            return {"note": "Comparaison impossible (données manquantes)"}
        try:
            R = 6371.0
            phi1, phi2 = math.radians(ip["latitude"]),  math.radians(win["latitude"])
            dlat = math.radians(win["latitude"]  - ip["latitude"])
            dlon = math.radians(win["longitude"] - ip["longitude"])
            a = math.sin(dlat/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlon/2)**2
            dist = round(R * 2 * math.asin(math.sqrt(a)), 3)
            return {
                "distance_km": dist,
                "distance_note": (
                    "Écart faible" if dist < 5 else
                    "Écart modéré" if dist < 20 else
                    "Écart important"
                ),
                "win_accuracy_m": win.get("accuracy_m"),
                "win_source":     win.get("position_source"),
            }
        except Exception as exc:
            return {"note": f"Calcul impossible : {exc}"}

    ip_data  = _get_ip()
    win_data = _get_windows()

    return {
        "generated_at":     datetime.datetime.now(datetime.UTC).isoformat(),
        "ip_location":      ip_data,
        "windows_location": win_data,
        "comparison":       _compare(ip_data, win_data),
    }, True

loadPrint()#c

def weather(lat: float = None, lon: float = None, city: str = None) -> dict:
    """
    Retourne un dictionnaire complet avec les données météo actuelles.

    Si lat/lon ne sont pas fournis, la localisation est détectée
    automatiquement via l'adresse IP publique (précision ~ville).

    Paramètres:
        lat  (float | None): Latitude  — None = détection automatique
        lon  (float | None): Longitude — None = détection automatique
        city (str   | None): Nom de la ville (optionnel, pour l'affichage)

    Retourne:
        dict: Données météo complètes ou dict avec clé "error" en cas d'échec.
    """

    def _get_location_auto() -> dict:
        """
        Détecte automatiquement la localisation via 3 méthodes en cascade :
        1. ip-api.com       — IP géolocation (précision ~ville)
        2. ipwho.is         — Fallback IP géolocation
        3. ipinfo.io        — Dernier recours IP géolocation

        Retourne un dict avec les clés : lat, lon, city, region, country,
        ip, isp, timezone  — ou lève une RuntimeError si tout échoue.
        """
        providers = [
            {
                "url": "http://ip-api.com/json/",
                "map": {
                    "lat":      lambda d: d.get("lat"),
                    "lon":      lambda d: d.get("lon"),
                    "city":     lambda d: d.get("city", ""),
                    "region":   lambda d: d.get("regionName", ""),
                    "country":  lambda d: d.get("country", ""),
                    "ip":       lambda d: d.get("query", ""),
                    "isp":      lambda d: d.get("isp", ""),
                    "timezone": lambda d: d.get("timezone", ""),
                },
                "ok": lambda d: d.get("status") == "success",
            },
            {
                "url": "https://ipwho.is/",
                "map": {
                    "lat":      lambda d: d.get("latitude"),
                    "lon":      lambda d: d.get("longitude"),
                    "city":     lambda d: d.get("city", ""),
                    "region":   lambda d: d.get("region", ""),
                    "country":  lambda d: d.get("country", ""),
                    "ip":       lambda d: d.get("ip", ""),
                    "isp":      lambda d: d.get("connection", {}).get("isp", ""),
                    "timezone": lambda d: d.get("timezone", {}).get("id", ""),
                },
                "ok": lambda d: d.get("success", False),
            },
            {
                "url": "https://ipinfo.io/json",
                "map": {
                    "lat":      lambda d: float(d.get("loc", "0,0").split(",")[0]),
                    "lon":      lambda d: float(d.get("loc", "0,0").split(",")[1]),
                    "city":     lambda d: d.get("city", ""),
                    "region":   lambda d: d.get("region", ""),
                    "country":  lambda d: d.get("country", ""),
                    "ip":       lambda d: d.get("ip", ""),
                    "isp":      lambda d: d.get("org", ""),
                    "timezone": lambda d: d.get("timezone", ""),
                },
                "ok": lambda d: "loc" in d,
            },
        ]

        for provider in providers:
            try:
                resp = requests.get(provider["url"], timeout=5,
                                    headers={"User-Agent": "WeatherApp/1.0"})
                resp.raise_for_status()
                data = resp.json()
                if provider["ok"](data):
                    m = provider["map"]
                    return {key: fn(data) for key, fn in m.items()}
            except Exception:
                continue  # essaie le prochain fournisseur

        raise RuntimeError(
            "Impossible de détecter la localisation automatiquement "
            "(tous les fournisseurs IP ont échoué)."
        )

    # ── Détection automatique de la localisation ──────────────────────────────
    auto_location = {}
    if lat is None or lon is None:
        try:
            auto_location = _get_location_auto()
            lat  = auto_location["lat"]
            lon  = auto_location["lon"]
            city = city or auto_location.get("city", "")
        except RuntimeError as e:
            return {"error": str(e)}

    # --- 1. Météo actuelle + prévisions horaires/journalières ---
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ],
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
            "uv_index",
            "visibility",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "sunrise",
            "sunset",
            "daylight_duration",
            "uv_index_max",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
        ],
        "timezone": auto_location.get("timezone") or "auto",
        "forecast_days": 7,
    }

    # --- 2. Géocodage inverse pour obtenir l'adresse complète ---
    geo_url = "https://nominatim.openstreetmap.org/reverse"
    geo_params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
    }

    # Codes météo WMO → description lisible
    WMO_CODES = {
        0: "Ciel dégagé", 1: "Principalement dégagé", 2: "Partiellement nuageux",
        3: "Couvert", 45: "Brouillard", 48: "Brouillard givrant",
        51: "Bruine légère", 53: "Bruine modérée", 55: "Bruine dense",
        61: "Pluie légère", 63: "Pluie modérée", 65: "Pluie forte",
        71: "Neige légère", 73: "Neige modérée", 75: "Neige forte",
        77: "Grains de neige", 80: "Averses légères", 81: "Averses modérées",
        82: "Averses violentes", 85: "Averses de neige légères",
        86: "Averses de neige fortes", 95: "Orage", 96: "Orage avec grêle légère",
        99: "Orage avec grêle forte",
    }

    try:
        w_resp = requests.get(weather_url, params=weather_params, timeout=10)
        w_resp.raise_for_status()
        w_data = w_resp.json()
    except requests.RequestException as e:
        return {"error": f"Impossible de récupérer la météo : {e}"}

    try:
        g_resp = requests.get(geo_url, params=geo_params,
                              headers={"User-Agent": "WeatherApp/1.0"}, timeout=5)
        g_resp.raise_for_status()
        g_data = g_resp.json()
        address = g_data.get("display_name", city)
        address_details = g_data.get("address", {})
    except requests.RequestException:
        address = city
        address_details = {}

    cur = w_data.get("current", {})
    daily = w_data.get("daily", {})
    hourly = w_data.get("hourly", {})
    units = w_data.get("current_units", {})

    # Index de l'heure actuelle dans les données horaires
    now_iso = cur.get("time", "")
    hourly_times = hourly.get("time", [])
    try:
        hour_idx = hourly_times.index(now_iso)
    except ValueError:
        hour_idx = 0

    weather_code = cur.get("weather_code", -1)

    result = {
        # ── Localisation ──────────────────────────────────────────────
        "location": {
            "city": address_details.get("city") or address_details.get("town") or city,
            "region": address_details.get("state", ""),
            "country": address_details.get("country", ""),
            "timezone": w_data.get("timezone", ""),
            "ip": auto_location.get("ip", ""),
            "isp": auto_location.get("isp", ""),
            "geolocation_method": "ip-geolocation (auto)" if auto_location else "manuel",
        },

        # ── Conditions actuelles ──────────────────────────────────────
        "current": {
            "timestamp": cur.get("time"),
            "is_day": bool(cur.get("is_day", 1)),
            "weather_code": weather_code,
            "condition": WMO_CODES.get(weather_code, "Inconnu"),
            "temperature_c": cur.get("temperature_2m"),
            "feels_like_c": cur.get("apparent_temperature"),
            "humidity_percent": cur.get("relative_humidity_2m"),
            "precipitation_mm": cur.get("precipitation"),
            "rain_mm": cur.get("rain"),
            "snowfall_cm": cur.get("snowfall"),
            "cloud_cover_percent": cur.get("cloud_cover"),
            "pressure_hpa": cur.get("pressure_msl"),
            "surface_pressure_hpa": cur.get("surface_pressure"),
            "wind_speed_kmh": cur.get("wind_speed_10m"),
            "wind_direction_deg": cur.get("wind_direction_10m"),
            "wind_gusts_kmh": cur.get("wind_gusts_10m"),
        },

        # ── Données horaires (heure actuelle) ────────────────────────
        "current_hour_forecast": {
            "precipitation_probability_percent": (
                hourly.get("precipitation_probability", [None])[hour_idx]
            ),
            "uv_index": hourly.get("uv_index", [None])[hour_idx],
            "visibility_m": hourly.get("visibility", [None])[hour_idx],
        },

        # ── Prévisions 7 jours ────────────────────────────────────────
        "daily_forecast": [
            {
                "date": daily["time"][i],
                "condition": WMO_CODES.get(daily["weather_code"][i], "Inconnu"),
                "weather_code": daily["weather_code"][i],
                "temp_max_c": daily["temperature_2m_max"][i],
                "temp_min_c": daily["temperature_2m_min"][i],
                "feels_like_max_c": daily["apparent_temperature_max"][i],
                "feels_like_min_c": daily["apparent_temperature_min"][i],
                "sunrise": daily["sunrise"][i],
                "sunset": daily["sunset"][i],
                "daylight_duration_sec": daily["daylight_duration"][i],
                "uv_index_max": daily["uv_index_max"][i],
                "precipitation_sum_mm": daily["precipitation_sum"][i],
                "precipitation_probability_max_percent": daily["precipitation_probability_max"][i],
                "wind_speed_max_kmh": daily["wind_speed_10m_max"][i],
                "wind_gusts_max_kmh": daily["wind_gusts_10m_max"][i],
            }
            for i in range(len(daily.get("time", [])))
        ],

        # ── Métadonnées ───────────────────────────────────────────────
        "meta": {
            "source": "Open-Meteo (https://open-meteo.com)",
            "geocoding": "OpenStreetMap Nominatim",
            "fetched_at": datetime.datetime.now().isoformat(),
            "units": {
                "temperature": "°C",
                "wind_speed": "km/h",
                "precipitation": "mm",
                "snowfall": "cm",
                "pressure": "hPa",
                "visibility": "mètres",
            },
        },
    }

    return result

def getWeather():
    # try:
    data = weather()
    
    # Vérifier si une erreur s'est produite
    # print( json.dumps( indent=4, obj=data ) )
    if "error" in str( data ):
        log( "Exception when get weather", data["error"], "error" )
        return "Erreur pour obtenir la météo", False
    log( "Result raw getWeather", data, "debug" )
    current = data["current"]
    forecast = data["daily_forecast"][0]

    # print( "Getting localisation..." )
    location, _ = getLocalisation()
    log( "Result raw getLocalisaiton", location, "debug" )
    # print( json.dumps( location, indent=4 ) )
    location = location["ip_location"]
    # print( json.dumps( location, indent=4 ) )
    wind_direction = ""
    # print( f"{current["wind_direction_deg"]=}" )
    wind_degrees = current["wind_direction_deg"]
    if 360 - 22.5 < wind_degrees or wind_degrees < 22.5:
        wind_direction = "nord"
    elif wind_degrees < 67.5:
        wind_direction = "nord-est"
    elif wind_degrees < 112.5:
        wind_direction = "est"
    elif wind_degrees < 157.5:
        wind_direction = "sud-est"
    elif wind_degrees < 202.5:
        wind_direction = "sud"
    elif wind_degrees < 247.5:
        wind_direction = "sud-ouest"
    elif wind_degrees < 292.5:
        wind_direction = "ouest"
    elif wind_degrees < 337.5:
        wind_direction = "nord-ouest"
    else:
        wind_direction = "nord"

    # print( f"{location=}, {current=}, {wind_direction=}" )
    try:
        to_return = f"""
En ce moment, à {location["city"]}, {location["region"]}, {location["country"]}, le {current["timestamp"]}, il fait {current["temperature_c"]}°C.
La température ressentie est de {current["feels_like_c"]}°C avec une humidité de {current["humidity_percent"]} %.
Le ciel est {current["condition"]} et recouvert de nuages à {current["cloud_cover_percent"]} %.
Il y a {current["precipitation_mm"]} mm de précipitations, {current["rain_mm"]} mm de pluie et {current["snowfall_cm"]} cm de neige.
Le vent souffle à {current["wind_speed_kmh"]} km/h avec des rafales à {current["wind_gusts_kmh"]} km/h en provenance du {wind_direction}.

La condition prévue est {forecast["condition"]}, avec une température maximale de {forecast["temp_max_c"]}°C ressentie {forecast["feels_like_max_c"]}°C et une température minimale de {forecast["temp_min_c"]}°C ressentie {forecast["feels_like_min_c"]}°C.
Le soleil se lèvera à {forecast["sunrise"]} et se couchera à {forecast["sunset"]}.
La durée du jour sera de {forecast["daylight_duration_sec"]} secondes. L'indice UV sera de {forecast["uv_index_max"]}.
Les précipitations attendues sont de {forecast["precipitation_sum_mm"]} mm avec une probabilité de {forecast["precipitation_probability_max_percent"]} %.
Les rafales de vent seront de maximum {forecast["wind_gusts_max_kmh"]} km/h avec du vent à maximum {forecast["wind_speed_max_kmh"]} km/h.
"""
    except Exception as e:
        log( "Error while creating simple text for weather", {"error": str( e ), "location": location, "current": current, "forecast": forecast}, "error" )
        to_return = "Erreur lors de l'obtention de la météo"
    # to_return = {
    #     "localisation": location,
    #     "current": current,
    #     "forecast": forecast
    # }
    print( to_return )
    return to_return, True
    # except Exception as e:
    #     log( "Exception when get weather", str( e ), "error" )
        # return "Erreur pour obtenir la météo", False


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
        sendNotification( f"email envoyé à {receiver}" )
        log( "Email sent", "", 'info' )
    except Exception as e:
        log( "Email error", str( e ), 'error' )
        return "Envoie du courriel raté", True
    
    return "Envoie du courriel réussi", False

loadPrint()#c

# =====================
# TOOL: sleepSystem
# =====================
def sleepSystem( exception, audio ):
    global conversation, called, AUDIO, fast_called, check_audio_call
    time.sleep( 1 )
    Sound.waitForSoundTofinish()
    fast_called = False
    AUDIO = True
    GUI.textInput( False )
    GUI.setTextToDisplay( '' )
    GUI.displayRika( False )
    called = False
    # conversation.append(
    #     {
    #         "role": "system",
    #         "content": f"{moment()}"
    #     }
    # )
    with conversation_mutex:
        if SERVER_URL:
            requests.post( f"{SERVER_URL}/{SET_CONVERSATION}", json=conversation )
        Json.write( conversation, CONVERSATION_PATH )
        conversation = None
    if audio:
        Sound.playFile( CONFIRMATION_SOUND, True )
    if exception:
        raise ExitAgent()
    # exit( 0 )

loadPrint()#c

# =====================
# TOOL: getImage
# =====================
# cap.release()
def getImage( type ):
    if type == "screenshot":
        with mss.mss() as sct:
            # Obtenir la position du curseur
            from ctypes import Structure, POINTER, pointer, CDLL, c_long
            
            class POINT(Structure):
                _fields_ = [("x", c_long), ("y", c_long)]
            
            GetCursorPos = CDLL('user32').GetCursorPos
            pt = POINT()
            GetCursorPos(pointer(pt))
            cursor_x, cursor_y = pt.x, pt.y
            
            # Trouver l'écran contenant le curseur
            cursor_monitor = None
            for i, monitor in enumerate( sct.monitors[1:], start=1 ):
                if (monitor["left"] <= cursor_x <= monitor["left"] + monitor["width"] and
                    monitor["top"] <= cursor_y <= monitor["top"] + monitor["height"]):
                    cursor_monitor = (i, monitor)
                    break
            
            # Si aucun écran n'est trouvé, utiliser le premier écran
            if cursor_monitor is None:
                cursor_monitor = (1, sct.monitors[1])
            
            # Capturer uniquement l'écran du curseur
            i, monitor = cursor_monitor
            shot = sct.grab( monitor )
            img = Image.frombytes( "RGB", shot.size, shot.rgb )
            path = os.path.join( SCREENSHOT_DIR, f"screen_{i}.jpg" )
            img.save( path )

        return f"Screenshot capturé de l'écran {i}"

    if type == "webcam":
        cap = cv2.VideoCapture( getCameraIndex( "USB" ) )
        ret, frame = cap.read()
        if not ret:
            return "Erreur webcam"
        cap.release()
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

    log( "analyseImage", {"type": type, "prompt": prompt, "renew": renew}, "debug" )

    if type == "screenshot":
        files = sorted( 
            f for f in os.listdir( SCREENSHOT_DIR )
            if f.lower().endswith( ".jpg" )
        )

        if not files:
            if renew:
                return "Aucun screenshot disponible", True
            else:
                return analyseImage( type, prompt, True )
        images = []
        for file in files:
            path = os.path.join( SCREENSHOT_DIR, file )
            image_b64 = image_to_base64( path )
            images.append( image_b64 )

    elif type == "webcam":
        if not os.path.exists( WEBCAM_PATH ):
            return "Aucune image webcam disponible", True

        image_b64 = image_to_base64( WEBCAM_PATH )

    else:
        return "Type invalide", True

    print( "ask model for vision" )
    try:
        # response = Model.askModel( VISION_MODEL, messages, "high", MAX_RETRIES, Model.Verification.rawResponse )
        response = Model.askVisionModel( image_b64, prompt )
    except NoResponseError as e:
        return f"Erreur lors de l'anaylse de l'image", True

    return f"voici le contenu de image. Ne te concentre que sur l'essentiel que {USERNAME} t'a demandé. Fait ce que {USERNAME} te demande de faire avec : " + response, True

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
    for i in range( MAX_RETRIES ):
        try:
#             summary = Model.askModel(
#                 SIMPLE_MODEL,
#                 [
#                     {
#                         "role": "system",
#                         "content": """
# Ressort moi uniquement du Json avec ce format exact, sans rien d'autre :
# {
#     "message": "résumé du texte à dire à l'utilisateur, en français, concis. Garde le contenu général pour le raccourcir",
# }
# Ne met pas de caractères de mise en forme dans le message, comme des astérisques, des accents, ou des emojis.
# Juste du texte brut, sans retour à la ligne.
# Ne coupe pas les phrases au milieu, garde les phrases entières.
# Raccourcis le message d'origine sans omettre d'informations importantes.
# Le résultat doit OBLIGATOIREMENT avoir moins de 50 mots
# Garde le plus d'informations importantes possible en respectant la limite de mots
#         """,
#                         "name": "instructions"
#                     },
#                     {
#                         "role": "user",
#                         "content": response
#                     }
#                 ],
#                 "none",
#                 MAX_RETRIES,
#                 Model.Verification.isJson
#             )
            summary = Model.askModel(
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
                Model.Verification.isJson
            )
        except NoResponseError as e:
            return response

    try:
        return json.loads( summary )["message"]
    except JSONDecodeError:
        return summary

loadPrint()#c

def treatTextResponse( response: str ):
    return response.replace( "**", '' ).replace( "‑", "-" )

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

    Sound.waitForSoundTofinish()
    Sound.generateVoice( say_response, VOICE )
    Sound.playVoice()

loadPrint()#c

def getUserInput():
    # print( "getting input" )
    user_input = ''
    if AUDIO:
        Sound.waitForSoundTofinish()
        # user_input = Sound.listen()
        user_input = Sound.listenSRWhisper()
        # print( user_input )
    else:
        # user_input = input( "YOU > " )
        while True:
            # print( GUI.getTextInputState() )
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
    print( f"YOU > {user_input}" )
    return user_input

loadPrint()#c

def treatResponse( response: str ):
    if len( response ) != 0:
        treated_text = treatTextResponse( response )
        GUI.setTextToDisplay( treated_text )
        if AUDIO:
            treatAudioResponse( response )
        print( f"{ASSISTANT_NAME} >", treated_text )
    else:
        GUI.setTextToDisplay( response )

loadPrint()#c

# =====================
# MAIN LOOP
# =====================
def chat():
    global conversation, treating_response, prompt, fast_called

    incognito = False
    private_history = []
    
    april_fools_rickroll()
    if AUDIO:
        Sound.playFile( CONFIRMATION_SOUND, False )
    # print( "called" )

    # conversation.append(
    #     {
    #         "role": "system",
    #         "content": f"{moment()}"
    #     }
    # )

    while True:
        # print( f"{incognito=}" )
        # print( "getting emails" )

        if WIFI:
            agent_email_thread = ThreadWithReturnValue( target=getEmail, args=( EMAIL, EMAIL_PASSWORD ), name="read emails" )
            agent_email_thread.start()

            user_email_thread = ThreadWithReturnValue( target=getEmail, args=( USER_EMAIL, PASSWORD ), name="read user emails" )
            user_email_thread.start()
        
        # print( "asking user" )
        treating_response.join()
        # sendNotification( "Attente de votre message", "Rika attend votre message, vous pouvez maintenant parler" )
        if not fast_called:
            if AUDIO:
                print( "Talk..." )
            else:
                print( "Write..." )
        Sound.waitForSoundTofinish()
        if fast_called:
            user_input = prompt
        else:
            user_input = getUserInput()
        # WIFI = hasWifiAccess()
        if WIFI:
            emails = agent_email_thread.join()
            user_emails = user_email_thread.join()
            for email in emails:
                if not incognito:
                    # print( "adding to regular conversation" )
                    with conversation_mutex:
                        conversation.append(
                            {
                                "role": "user",
                                "content": "Email reçu sur l'adresse de l'agent :\n\n" + json.dumps( email, indent=4 ),
                                "name": "getEmail tool"
                            }
                        )
                else:
                    # print( "adding to private conversation" )
                    private_history.append(
                        {
                            "role": "user",
                            "content": "Email reçu sur l'adresse de l'agent :\n\n" + json.dumps( email, indent=4 ),
                            "name": "getEmail tool"
                        }
                    )
            for email in user_emails:
                if not incognito:
                    # print( "adding to regular conversation" )
                    with conversation_mutex:
                        conversation.append(
                            {
                                "role": "user",
                                "content": "Email reçu sur l'adresse de l'utilisateur :\n\n" + json.dumps( email, indent=4 ),
                                "name": "getEmail tool"
                            }
                        )
                else:
                    # print( "adding to private conversation" )
                    private_history.append(
                        {
                            "role": "user",
                            "content": "Email reçu sur l'adresse de l'utilisateur :\n\n" + json.dumps( email, indent=4 ),
                            "name": "getEmail tool"
                        }
                    )

        if type( user_input ) == str:

            # print( f"{type( conversation )=}" )
            # print( f"{conversation=}" )
            if not incognito:
                # print( "adding to regular conversation", not incognito )
                with conversation_mutex:
                    conversation.append(
                        {
                            "role": "user",
                            "content": user_input,
                            "name": USERNAME
                        }
                    )
            else:
                # print( "adding to private conversation", incognito )
                private_history.append(
                    {
                        "role": "user",
                        "content": user_input,
                        "name": USERNAME
                    }
                )

            response = None
            # while True:
            print( "ask model for chatting (1)" )

            with conversation_mutex:
                tmp = conversation.copy()
            if incognito:
                print( "using private conversation" )
                tmp.extend( private_history )
            try:
                # response = Model.askModel( MAIN_MODEL, tmp, "high", MAX_RETRIES, Model.Verification.isJson )
                response = Model.askModel( tmp, Model.Verification.isJson )
            except NoResponseError as e:
                response = json.dumps(
                    {
                        "message": str( e ),
                        "tools": []
                    }
                )

            content = json.loads( response )
            
            try:
                _ = content["tools"]
            except KeyError:
                content["tools"] = []

            treating_response = threading.Thread( target=treatResponse, args=( content["message"], ), name="process model response" )
            treating_response.start()

            if not incognito:
                # print( "adding to regular conversation" )
                with conversation_mutex:
                    conversation.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )
            else:
                # print( "adding to private conversation" )
                private_history.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )
            
            if fast_called and content["tools"] == []:
                treating_response.join()
                Sound.waitForSoundTofinish()
                log( "Use sleepSystem", "call 1", "info" )
                sleepSystem( True, AUDIO )
            # treated_text = treadTextResponse( content["message"] )
            
            # print( f"{ASSISTANT_NAME} >", treated_text )
            # GUI.setTextToDisplay( treated_text )
            # if AUDIO:
            #     treatAudioResponse( content["message"] )
            
            not_understand = False
            do_response = False
            responses = []
            try:
                while len( content["tools"] ) != 0:
                    responses = []
                    for tool in content["tools"]:
                        params = tool["params"]
                        print( f"Using {tool["name"]} tool\n\n" )
                        log( "Using tool", tool, "info" )
                        if tool["name"] == "analyseOldImage":
                            result, do_response = analyseImage( params["source"], params["prompt"], False )
                        elif tool["name"] == "analyseNewImage":
                            result, do_response = analyseImage( params["source"], params["prompt"], True )
                        elif tool["name"] == "sendEmail":
                            if WIFI:
                                result, do_response = sendEmail( params["receiver"], params["subject"], params["content"] )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "openLink":
                            if WIFI:
                                try:
                                    query = params["query"]
                                    result, do_response = openLink( query, False )
                                except KeyError:
                                    query = params["link"]
                                    result, do_response = openLink( query, True )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "getLocalisation":
                            if WIFI:
                                result, do_response = getLocalisation()
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "getWeather":
                            if WIFI:
                                result, do_response = getWeather()
                            else:
                                result, do_response =f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "getTime":
                            result, do_response = getTime()
                        elif tool["name"] == "createChart":
                            if fast_called:
                                result, do_response = "Erreur lors de la création du diagramme, veuillez aller en conversation longue pour l'affichage du diagramme", True
                            else:
                                result, do_response = createChart( params["type"], params["title"], params["data"], params["x-axis-title"], params["y-axis-title"] )
                        elif tool["name"] == "createWidget":
                            if WIFI:
                                result, do_response = createWidget( params["description"] )
                            else:
                                result, do_response =f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "startChrono":
                            result, do_response = startChrono()
                        elif tool["name"] == "stopChrono":
                            result, do_response = getChrono()
                        elif tool["name"] == "startTimer":
                            result, do_response = startTimer( params["message"], params["duration"] )
                        elif tool["name"] == "getRemainingTime":
                            result, do_response = getRemainingTimerTime()
                        elif tool["name"] == "openApp":
                            result, do_response = openApp( params["app"] )
                        elif tool["name"] == "doProtocol":
                            result, do_response = doProtocol( params["protocol"] )
                        elif tool["name"] == "playMusic":
                            if WIFI:
                                # print( "ceci sera affiché" )
                                # print( params )
                                try:
                                    _ = params["volume"]
                                except KeyError:
                                    params["volume"] = DEFAULT_VOLUME
                                result, do_response = playMusic( params["search"], params["type"], params["device"], params["volume"] )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "recognizeMusic":
                            if WIFI:
                                result, do_response = recognizeMusic()
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "setMusicState":
                            if WIFI:
                                result, do_response = setMusicState( params["state"] )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "changeMusicTrack":
                            if WIFI:
                                result, do_response = changeMusicTrack( params["target"] )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "saveFile":
                            result, do_response = saveFile( params["name"], params["content"] )
                        elif tool["name"] == "webSearch":
                            if WIFI:
                                result, do_response = webSearch( params["query"] )
                            else:
                                result, do_response = f"Aucune connexion internet, impossible d'accéder à l'outil {tool["name"]}", True
                        elif tool["name"] == "setIncognito":
                            incognito = params["value"]
                            if incognito:
                                result = "Le mode incognito est activé"
                                sendNotification( "Mode incognito : " + str( result ) )
                            else:
                                with conversation_mutex:
                                    conversation.append(
                                        {
                                            "role": "system",
                                            "content": "... Conversation masquée ..."
                                        }
                                    )
                                result = "Le mode incognito est désactivé"
                                sendNotification( "Mode incognito : " + str( result ) )
                                private_history = []
                            do_response = False
                        elif tool["name"] == "getIncognito":
                            if incognito:
                                result = "Le mode incognito est activé"
                            else:
                                result = "Le mode incognito est désactivé"
                            do_response = True
                        elif tool["name"] == "notUnderstand":
                            if not fast_called:
                                not_understand = True
                                break
                            else:
                                treating_response.join()
                                Sound.waitForSoundTofinish()
                                log( "Use sleepSystem", "call 2", "info" )
                                sleepSystem( True, AUDIO )
                        elif tool["name"] == "sleepSystem":
                            treating_response.join()
                            Sound.waitForSoundTofinish()
                            log( "Use sleepSystem", "call 3", "info" )
                            sleepSystem( True, AUDIO )
                        else:
                            result = f"No tool found for {tool["name"]}"
                        print( "tool use finished" )
                        
                        if not not_understand:
                            if type( result ) == str:
                                to_append = {
                                    "role": "user",
                                    "content": result,
                                    "name": f"{tool["name"]} tool"
                                }
                            elif type( result ) == dict:
                                to_append = {
                                    "role": "user",
                                    "content": json.dumps( result ),
                                    "name": f"{tool["name"]} tool"
                                }
                            else:
                                to_append = {
                                    "role": "user",
                                    "content": str( result ),
                                    "name": f"{tool["name"]} tool"
                                }
                            if not incognito:
                                # print( "adding to regular conversation" )
                                with conversation_mutex:
                                    conversation.append( to_append )
                            else:
                                # print( "adding to private conversation" )
                                private_history.append( to_append )
                        # print( f"{do_response=}, {responses=}" )
                        responses.append( do_response )
                    

                    for response in responses:
                        if response:
                            do_response = True
                            break
                    
                    if fast_called and not do_response:
                        treating_response.join()
                        Sound.waitForSoundTofinish()
                        log( "Use sleepSystem", "call 4", "info" )
                        sleepSystem( True, AUDIO )
                    # print( f"{do_response=}" )
                    if not_understand:
                        content["tools"] = []
                        break
                    if do_response:
                        treating_response.join()
                        
                        print( "ask model for chatting (2)" )
                        with conversation_mutex:
                            tmp = conversation.copy()
                        if incognito:
                            print( "using private conversation" )
                            tmp.extend( private_history )
                        try:
                            # response = Model.askModel( MAIN_MODEL, tmp, "high", MAX_RETRIES, Model.Verification.isJson )
                            response = Model.askModel( tmp, Model.Verification.isJson )
                        except NoResponseError as e:
                            response = json.dumps(
                                {
                                    "message": str( e ),
                                    "tools": []
                                }
                            )
                        content = json.loads( response )
                        try:
                            _ = content["tools"]
                        except KeyError:
                            content["tools"] = []
                        treating_response = threading.Thread( target=treatResponse, args=( content["message"], ), name="process model response" )
                        treating_response.start()
                        print( "append to convesation" )
                        if not incognito:
                            # print( "adding to regular conversation" )
                            with conversation_mutex:
                                conversation.append(
                                    {
                                        "role": "assistant",
                                        "content": response
                                    }
                                )
                        else:
                            # print( "adding to private conversation" )
                            private_history.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )
                        
                        if fast_called and content["tools"] == []:
                            treating_response.join()
                            Sound.waitForSoundTofinish()
                            log( "Use sleepSystem", "call 5", "info" )
                            sleepSystem( True, AUDIO )
                            
                        # treated_text = treadTextResponse( content["message"] )
                        # GUI.setTextToDisplay( treated_text )
                        # print( f"{ASSISTANT_NAME} >", treated_text )
                        # if AUDIO:
                        #     treatAudioResponse( content["message"] )
                    else:
                        break
            except KeyError:
                pass

loadPrint()#c

time.sleep( 0.5 )


# =====================
# START
# =====================
try:
    if __name__ == "__main__":
        # print( "" )
        # run_api.run()
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
                    with conversation_mutex:
                        conversation = Json.read( CONVERSATION_PATH )
                        if SERVER_URL:
                            data = requests.get( f"{SERVER_URL}/{GET_CONVERSATION}" )
                            conversation = data.json()
                            del data
                        
                        while len( conversation ) < 2:
                            conversation.append( 0 )

                        conversation[0] = {
                            "role": "system",
                            "name": "instructions",
                            "content": base_message
                        }

                        with open( USERNOTE_DIRECTORY, "r", encoding="utf-8" ) as f:
                            user_note = f.read()

                        conversation[1] = {
                            "role": "user",
                            "name": USERNAME,
                            "content": user_note
                        }

                    chat()
                except ExitAgent:
                    GUI.displayRika( False )
                    print( "Zzz..." )
            time.sleep( 2 )


except KeyboardInterrupt:
    GUI.quitGUI()
    Json.write( conversation, CONVERSATION_PATH )
    # Sauvegarde brute pour debug
    for message in conversation:
        if message["role"] == "assistant":
            message["content"] = json.loads( message["content"] )
    Json.write( conversation, f"{DEBUG_PATH}conversation-debug.json" )


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