# import json
# import requests

# class Json:
#     def write( informations: dict, json_name: str ):
#         json_object = json.dumps( informations, indent=4 )
#         with open( json_name, 'w', encoding="utf-8" ) as outfile:
#             outfile.write( json_object )
#     def read( json_name: str ):
#         with open( json_name, 'r', encoding="utf-8" ) as infile:
#             informations = json.load( infile )
#         return informations

# conversation = Json.read( "./conversation.json" )

# requests.post( "https://rikavinada9952.pythonanywhere.com/setConversation", json=conversation )


import os
os.system("")  # Enables ANSI escape sequences on Windows

# Colors
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

print(f"{RED}This is red text{RESET}")
print(f"{GREEN}This is green text{RESET}")
