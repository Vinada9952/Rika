import os
from RIKAgroq import Json
from RIKAgroq import Sound

os.system( "pip install -r requirement.txt" )
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
        print( "Disez le nom de l'agent dans votre microphone..." )
        listen = Sound.listen()
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
    "server-url": "localhost:5000"
}

Json.write( base_settings, "./settings.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/protocols/protocols.json" )
Json.write( [], "./assets/contacts.json" )