import json
import requests

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

conversation = Json.read( "./conversation.json" )

requests.post( "https://vinada9952rika.pythonanywhere.com/setConversation", json=conversation )