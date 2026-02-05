from groq import Groq
import os
from Vincent import Sound


if os.path.exists( "./GROQ_API.key" ):
    with open( "./GROQ_API.key", "r" ) as f:
        API_KEY = f.read()
else:
    API_KEY = input( "API Key (on https://console.groq.com/keys) : " )
    with open( "./GROQ_API.key", 'x' ) as f:
        f.write( API_KEY )

client = Groq(api_key=API_KEY)

conversation = [
    {
        "role": "system",
        "content": "Tu es JARVIS, développé et utilisé par Vincent Tuê Minh Boucher, mais appelle moi tout simplement Vincent."
    }
]