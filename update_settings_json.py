import json
import os

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ) -> dict:
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

settings_list = {
    "\"assistant-name\"": "Rika",
    "[api-keys]": [""],
    "max-api-retry": 10,
    "[call-names]": [
            "ikea",
            "reka",
            "rica",
            "richard",
            "fr\u00e9quence",
            "rika",
            "requin",
            "rita",
            "ricardo",
            "rik",
            "riga",
            "richelieu",
            "robert",
            "ricard"
        ],
    "\"hotkey\"": "alt+space",
    "\"reset-protocol-name\"": "No Way Home",
    "audio": True,
    "audio-duration-threshold": 15,
    "\"voice\"": "fr-CA-SylvieNeural",
    "\"screenshot-path\"": "./cache/screenshots/",
    "\"cache-path\"": "./cache/",
    "\"webcam-path\"": "./cache/captured.jpg",
    "\"protocols-path\"": "./assets/protocols/protocols.json",
    "\"contacts-path\"": "./assets/contacts.json",
    "\"data-model\"": "llama-3.1-8b-instant",
    "\"main-model\"": "openai/gpt-oss-120b",
    "\"vision-model\"": "meta-llama/llama-4-scout-17b-16e-instruct",
    "\"web-model\"": "groq/compound",
    "\"agent-email-adress\"": None,
    "\"agent-email-pwd\"": None,
    "\"smtp-server\"": "smtp.gmail.com",
    "smtp-port": 587,
    "\"username\"": None,
    "\"user-email\"": None,
    "\"server-url\"": None,
    "\"server-setconversation\"": "setConversation",
    "\"server-getconversation\"": "getConversation",
    "[gui-color]": [3, 232, 252],
    "\"font-path\"": "./assets/gui/Nasalization Rg.otf",
    "[apps-path-getenv]": [
        {
            "key": "ProgramFiles",
            "default": "C:/Program Files"
        },
        {
            "key": "ProgramFiles(x86)",
            "default": "C:/Program Files (x86)"
        }
    ],
    "[apps-path-expand-user]": [
        "~/AppData/Local",
        "~/AppData/Roaming",
        "~/Desktop",
        "~/Documents"
    ],
    "[apps-path-normal]": [],
}

new_template = {
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
        "cache": {
            "screenshots": "\"screenshot-path\"",
            "cache": "\"cache-path\"",
            "webcam": "\"webcam-path\""
        },
        "assets": {
            "protocols": "\"protocols-path\"",
            "contacts": "\"contacts-path\""
        },
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
}

current_template = Json.read( "./current_setting.template" )
current_settings = Json.read( "./settings.json" )

def findKeysFromValue( d: dict, value: str ) -> list:
    for k, v in d.items():
        if v == value:
            return [k]
        elif isinstance( v, dict ):
            nested = findKeysFromValue( v, value )
            if nested:
                return [k] + nested
    return []

def getValuePath( data, path, default=None ):
    value = data
    for key in path:
        if isinstance( value, dict ) and key in value:
            value = value[ key ]
        else:
            return default
    return value

def setValueFromPath(data: dict, path: list, value):
    if not path:
        return value

    key = path[0]

    if len(path) == 1:
        data[key] = value
        return data

    if key not in data or not isinstance(data[key], dict):
        data[key] = {}

    data[key] = setValueFromPath(data[key], path[1:], value)
    return data

for data in settings_list:
    path = findKeysFromValue( current_template, data )
    value = getValuePath( current_settings, path )
    settings_list[data] = value

Json.write( new_template, "./current_setting.template" )
new_settings = new_template

for key in settings_list.keys():
    data = settings_list[key]
    path = findKeysFromValue( new_template, key )
    new_settings = setValueFromPath( new_settings, path, data )
    pass

Json.write( new_settings, "./settings.json" )