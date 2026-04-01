import os
os.system( "pip install -r requirement.txt" )
import json
import speech_recognition as sr

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

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

os.makedirs( "./cache", True )
os.makedirs( "./cache/screenshots", True )
os.makedirs( "./assets/protocols/", True )

api_key = input( "Clé API groq (https://console.groq.com/keys) : " )
name = input( "Votre nom : " )
user = input( "Votre email : " )

ask = input( "Voulez vous modifier le nom de l'agent ? (o/n) : " )
if ask == 'o':
    assistant_name = input( "Nom de l'agent : " )
    call_names = []
    calibration = 0
    while True:
        print( "Dites le nom de l'agent dans votre microphone..." )
        listen = listen()
        print( "patientez..." )
        if listen not in call_names:
            call_names.append( listen )
        else:
            calibration += 1
        if calibration == 5:
            break
else:
    assistant_name = "Rika"
    call_names = [
        "ikea",
        "reka",
        "rica",
        "richard",
        "rika",
        "requin",
        "ricardo",
        "rik",
        "riga",
        "richelieu",
        "robert",
        "ricard"
    ]

ask = input( "Voulez vous mettre un email pour l'agent ? (o/n) : " )
if ask.lower() == 'o':
    email = input( "Email de L'agent : " )
    pwd = input( "Mot de passe de l'agent pour l'email (https://myaccount.google.com/apppasswords)" )
else:
    email = "No Email Available"
    pwd = "No Email Available"

base_settings = {
    "assistant-name": "Rika",
    "api-keys": [
        api_key
    ],
    "max-api-retries": 10,
    "call": {
        "names": call_names,
        "hotkey": "ctrl+alt+r"
    },
    "audio": {
        "audio": True,
        "audio-duration-threshold": 15,
        "voice": "fr-CA-SylvieNeural"
    },
    "directories": {
        "screenshots": "/cache/screenshots/",
        "cache": "cache/",
        "webcam": "./cache/captured.jpg",
        "protocols": "./assets/protocols/protocols.json",
        "contacts": "./assets/contacts.json"
    },
    "models": {
        "main": "openai/gpt-oss-120b",
        "data": "llama-3.1-8b-instant",
        "vision": "meta-llama/llama-4-scout-17b-16e-instruct",
        "web": "groq/compound"
    },
    "email": {
        "email": email,
        "pwd": pwd,
        "smtp": {
            "server": "smtp.gmail.com",
            "port": 587
        },
        "user-email": {
            "name": name,
            "email": user
        }
    },
    "server": {
        "url": None,
        "set-conversation": "setConversation",
        "get-conversation": "getConversation"
    },
    "color": [ 3, 232, 252 ],
    "gui":{
        "color": [ 3, 232, 252 ],
        "font": "./assets/gui/Nasalization Rg.otf"
    },
    "reset-protocol-name": "Mémoire Saturée",
    "apps-path": {
        "get-env":[
            {
                "key": "ProgramFiles",
                "default": "C:/Program Files"
            },
            {
                "key": "ProgramFiles(x86)",
                "default": "C:/Program Files (x86)"
            }
        ],
        "expand-user": [
            "~/AppData/Local",
            "~/AppData/Roaming",
            "~/Desktop",
            "~/Documents"
        ],
        "normal": []
    }
}

Json.write( base_settings, "./settings.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/contacts.json" )
Json.write( [], "./assets/conversation.json" )
Json.write(
    {
        "assistant-name": "\"assistant-name\"",
        "api": {
            "api-keys": "[api-keys]",
            "max-api-retries": "max-api-retry"
        },
        "call": {
            "names": "[call-names]",
            "hotkey": "\"hotkey\""
        },
        "reset-protocol-name": "\"reset-protocol-name\"",
        "audio": {
            "audio": "audio",
            "audio-duration-threshold": "audio-duration-threshold",
            "voice": "\"voice\""
        },
        "directories": {
            "screenshots": "\"screenshot-path\"",
            "cache": "\"cache-path\"",
            "webcam": "\"webcam-path\"",
            "protocols": "\"protocols-path\"",
            "contacts": "\"contacts-path\"",
            "apps-path": {
                "get-env": "[apps-path-getenv]",
                "expand-user": "[apps-path-expand-user]",
                "normal": "[apps-path-normal]"
            }
        },
        "models": {
            "data": "\"data-model\"",
            "main": "\"main-model\"",
            "vision": "\"vision-model\"",
            "web": "\"web-model\""
        },
        "email": {
            "email": "\"agent-email-adress\"",
            "pwd": "\"agent-email-pwd\"",
            "smtp": {
                "server": "\"smtp-server\"",
                "port": "smtp-port"
            },
            "user-email": {
                "name": "\"username\"",
                "email": "\"user-email\""
            }
        },
        "server": {
            "url": "\"server-url\"",
            "set-conversation": "\"server-setconversation\"",
            "get-conversation": "\"server-getconversation\""
        },
        "gui":{
            "color": "[gui-color]",
            "font": "\"font-path\""
        }
    },
    "./current_setting.template"
)