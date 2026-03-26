import os
os.system( "pip install -r requirement.txt" )

from RIKAgroq import Json
from RIKAgroq import Sound
os.mkdir( "./cache" )
os.mkdir( "./cache/screenshots" )
os.mkdir( "./assets/protocols/" )

assistant_name = input( "Nom de l'agent : " )
api_key = input( "Clé API groq (https://console.groq.com/keys) : " )
email = input( "Email de L'agent : " )
pwd = input( "Mot de passe de l'agent pour l'email (https://myaccount.google.com/apppasswords)" )
name = input( "Votre nom : " )
user = input( "Votre email : " )

call_names = []
calibration = 0
while True:
    print( "Disez le nom de l'agent dans votre microphone..." )
    listen = Sound.listen()
    print( "patientez..." )
    if listen not in call_names:
        call_names.append( listen )
    else:
        calibration += 1
    if calibration == 5:
        break

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
        "data": "llama-3.1-8b-instant",
        "main": "openai/gpt-oss-120b",
        "vision": "meta-llama/llama-4-scout-17b-16e-instruct"
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
    "server-url": "localhost:5000"
}

Json.write( base_settings, "./settings.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/contacts.json" )