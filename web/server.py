import os
import json
import base64
import random
import asyncio
import requests
from flask import Flask, request, jsonify, send_file
from groq import Groq, APIStatusError
import edge_tts

# =====================
# CONFIG
# =====================

API_KEYS = [
    "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",
    "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"
]

client = Groq(api_key=API_KEYS[0])

MAIN_MODEL = "groq/compound"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
VOICE = "fr-CA-SylvieNeural"

MAX_RETRIES = 5

conversation = [
    {
        "role": "system",
        "name": "instructions",
        "content": """
Tu es un agent logiciel.

À CHAQUE MESSAGE, tu dois suivre ce raisonnement :
1) Décider si une action est nécessaire pour répondre correctement
2) Si OUI, tu DOIS utiliser un ou plusieurs outils
3) Si NON, tu réponds sans outil

Tu DOIS répondre STRICTEMENT en JSON, SANS AUCUN TEXTE EN DEHORS.

FORMAT OBLIGATOIRE :

{
  "message": "ce que tu dis à l'utilisateur",
  "tools": []
}

ou, si des actions sont nécessaires :

{
  "message": "ce que tu dis à l'utilisateur",
  "tools": [
    {
      "name": "openLink",
      "params": {
        "link": "https://www.google.com/search?q=latest+news+about+ai"
      }
    },
    {
      "name": "analyseImage",
      "params": {
        "source": "screenshot",
        "prompt": "Décris ce que tu vois sur tous les écrans"
      }
    }
  ]
}

OUTILS DISPONIBLES :

- getLocalisation
  - Obtenir la localisation de l'utilisateur
  - exemples de cas d'utilisation:
  -> Où suis-je ?

- sleepSystem
  - Te mettre en veille lorsque l'utilisateur n'a plus besoin de toi pour l'instant.
  - CE N'EST PAS UNE EXTINCTION DÉFNITIVE, l'utilisateur te rappellera après
  - quand appeler la fonction (exemples):
  -> Merci : oui
  -> Merci, est ce que tu peux me l'ouvrir ?
  -> Explique moi la thermodynamique : non
  -> Génère moi un code python qui dit Bonjour : non
  -> au revoir : oui
  -> allo : non
  -> bye : oui
  -> Connard, t'es pas bon : oui
  -> Description de personne : non
  -> je t'ai donné l'information : non
  -> est ce que tu te rappelles d'une partie d'échec que tu jouais ? : non
  -> Qui es Warren Buffet : non
  -> Qui es le PDG de Nvidia présentement : non

- notUnderstand
  - Quand tu ne comprends pas le prompt de l'utilisateur, utilise cet outil pour clarifier le prompt

- analyseImage
  - UTILISATION OBLIGATOIRE si tu dois analyser une image
  - params:
  -> source (string): "webcam" | "screenshot": source de l'image
  -> prompt (string): texte: ce que tu demandes de l'image
  -> renew (bool): true|false: capturer une nouvelle image (true) ou garder la dernière image capturé (false)
  - exemples de cas d'utilisation:
  -> Regarde
  -> Que vois-tu ?
  -> j'ai un bug dans mon code

- openApp
  - ouvrir une application dans la liste des applications autorisés
  - params:
  -> app (string): application à ouvrir
  - applications autorisés:
  -> spotify
  -> teams
  -> discord
  -> snapchat
  -> social
  -> vs code

- openLink
  - UTILISATION OBLIGATOIRE si l'utilisateur demande un lien
  - Avant de l'utiliser, vérifie toi-même sur internet si le lien fonctionne
  - params:
  -> link (string): lien à ouvrir dans un navigateur pour montrer à l'utilisateur
  - exemples de cas d'utilisation:
  -> Je veux voir une vidéo youtube
  -> trouve moi les scores des olympiques
  -> trouve moi une carte de montréal

RÈGLES IMPORTANTES :
- L’ordre des outils est l’ordre d’exécution
- Si l'utilisateur demande un lien, **NE DONNE PAS LE LIEN DANS LE MESSAGE**, mets toujours un tool openLink.
- Si aucune action n’est nécessaire, tools DOIT être []
- Ne JAMAIS écrire autre chose que du JSON
"""
    }
]

app = Flask(__name__)
os.makedirs("cache", exist_ok=True)

# =====================
# UTIL
# =====================

def image_to_base64_bytes(image_bytes):
    return base64.b64encode(image_bytes).decode()

# def generate_voice(text):
#     async def _gen():
#         communicate = edge_tts.Communicate(text, VOICE)
#         await communicate.save("cache/output.mp3")
#     asyncio.run(_gen())

def generate_voice(text):
    async def _gen():
        path = "cache/output.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(path)
        # Vérifie que le fichier existe
        if not os.path.exists(path):
            raise FileNotFoundError("Impossible de générer output.mp3")
        return path
    return asyncio.run(_gen())


# =====================
# TOOLS
# =====================

def getLocalisation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        return response.json()
    except:
        return {"error": "localisation failed"}

def analyseImage_base64(image_b64, prompt):
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_b64}"
                }
            }
        ]
    }]

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=messages
    )

    return response.choices[0].message.content

# =====================
# ROUTES
# =====================

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Rika Vocal</title>
</head>
<body>

<h1>🤖 RIKA VOCAL</h1>

<div id="chat"></div>

<button onclick="startListening()">🎤 Parler</button>

<br><br>
<video id="video" autoplay width="300"></video>

<script>
let recognition;
let video = document.getElementById("video");

// =====================
// WEBCAM
// =====================
window.onload = async function () {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Ton navigateur ne supporte pas getUserMedia");
        return;
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });
        video.srcObject = stream;
    } catch (err) {
        console.error("Erreur accès caméra/micro:", err);
    }

    // =====================
    // RECONNAISSANCE VOCALE
    // =====================
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("SpeechRecognition non supporté");
        return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "fr-FR";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function (event) {
        let transcript = event.results[0][0].transcript;

        document.getElementById("chat").innerHTML +=
            "<p><b>Vous:</b> " + transcript + "</p>";

        sendToServer(transcript);
    };

    recognition.onerror = function (event) {
        console.error("Erreur micro:", event.error);
    };
};

// =====================
// START LISTENING
// =====================
function startListening() {
    if (recognition) recognition.start();
}

// =====================
// ENVOI AU SERVEUR
// =====================
async function sendToServer(text) {

    // Capture webcam
    let canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    let ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    let image = canvas.toDataURL("image/jpeg");

    // Géolocalisation
    let location = await new Promise((resolve) => {
        navigator.geolocation.getCurrentPosition(pos => {
            resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude });
        }, () => resolve(null));
    });

    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: text,
            image: image,
            location: location
        })
    });

    let data = await response.json();

    document.getElementById("chat").innerHTML +=
        "<p><b>Rika:</b> " + data.message + "</p>";

    let audio = new Audio(data.audio);
    audio.play();
}

</script>

</body>
</html>
"""

@app.route("/getConversation", methods=["GET"])
def get_convo():
    return jsonify({"conversation": conversation})

@app.route("/chat", methods=["POST"])
def chat():
    print( "chat request received" )
    global conversation

    data = request.json
    user_message = data.get("message")
    webcam_image = data.get("image")
    user_location = data.get("location")

    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Localisation
    if user_location:
        conversation.append({
            "role": "user",
            "content": f"Localisation navigateur: {user_location}",
            "name": "browserLocation"
        })
    else:
        user_ip = request.remote_addr
        loc = getLocalisation(user_ip)
        conversation.append({
            "role": "user",
            "content": f"IP localisation: {loc}",
            "name": "ipLocation"
        })

    # Appel Groq
    for _ in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MAIN_MODEL,
                messages=conversation
            )
            break
        except APIStatusError as e:
            if e.status_code == 429:
                client.api_key = random.choice(API_KEYS)

    content = response.choices[0].message.content
    conversation.append({
        "role": "assistant",
        "content": content
    })

    parsed = json.loads(content)

    # Analyse image si envoyée
    if webcam_image:
        image_b64 = webcam_image.split(",")[1]
        vision_result = analyseImage_base64(
            image_b64,
            "Décris précisément cette image"
        )
        conversation.append({
            "role": "user",
            "content": vision_result,
            "name": "analyseImage tool"
        })

    # Génération voix
    generate_voice(parsed["message"])

    return jsonify({
        "message": parsed["message"],
        "audio": "/audio"
    })

@app.route("/audio")
def audio():
    return send_file("cache/output.mp3", mimetype="audio/mpeg")

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
