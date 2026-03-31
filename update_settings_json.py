import json

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

for data in settings_list:
    path = findKeysFromValue( current_template, data )
    value = getValuePath( current_settings, path )
    settings_list[data] = value

new_settings = {
    "assistant-name": settings_list["\"assistant-name\""],
    "api": {
        "api-keys": settings_list["[api-keys]"],
        "max-api-retries": settings_list["max-api-retry"]
    },
    "call": {
        "names": settings_list["[call-names]"],
        "hotkey": settings_list["\"hotkey\""]
    },
    "reset-protocol-name": settings_list["\"reset-protocol-name\""],
    "audio": {
        "audio": settings_list["audio"],
        "audio-duration-threshold": settings_list["audio-duration-threshold"],
        "voice": settings_list["\"voice\""]
    },
    "directories": {
        "screenshots": settings_list["\"screenshot-path\""],
        "cache": settings_list["\"cache-path\""],
        "webcam": settings_list["\"webcam-path\""],
        "protocols": settings_list["\"protocols-path\""],
        "contacts": settings_list["\"contacts-path\""],
        "apps-path": {
            "get-env": settings_list["[apps-path-getenv]"],
            "expand-user": settings_list["[apps-path-expand-user]"],
            "normal": settings_list["[apps-path-normal]"]
        }
    },
    "models": {
        "data": settings_list["\"data-model\""],
        "main": settings_list["\"main-model\""],
        "vision": settings_list["\"vision-model\""],
        "web": settings_list["\"web-model\""]
    },
    "email": {
        "email": settings_list["\"agent-email-adress\""],
        "pwd": settings_list["\"agent-email-pwd\""],
        "smtp": {
            "server": settings_list["\"smtp-server\""],
            "port": settings_list["smtp-port"]
        },
        "user-email": {
            "name": settings_list["\"username\""],
            "email": settings_list["\"user-email\""]
        }
    },
    "server": {
        "url": settings_list["\"server-url\""],
        "set-conversation": settings_list["\"server-setconversation\""],
        "get-conversation": settings_list["\"server-getconversation\""]
    },
    "gui":{
        "color": settings_list["[gui-color]"],
        "font": settings_list["\"font-path\""]
    }
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
}

Json.write( new_settings, "./settings.json" )
Json.write( new_template, "./current_setting.template" )