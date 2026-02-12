import os
import cv2
import base64
import json
import time
import mss
import requests
import webbrowser
import pyautogui
from groq import Groq
from groq import APIStatusError
from PIL import Image

# =====================
# CONFIG
# =====================
client = Groq(api_key="YOUR_API_KEY_HERE")

MAIN_MODEL = "groq/compound"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SCREENSHOT_DIR = "screenshots"
WEBCAM_PATH = "captured.jpg"
MAX_RETRIES = 5

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =====================
# TOOLS DECLARATION (LLM SIDE)
# =====================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "openLink",
            "description": "Ouvre un lien dans le navigateur",
            "parameters": {
                "type": "object",
                "properties": {
                    "link": {"type": "string"}
                },
                "required": ["link"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "openApp",
            "description": "Ouvre une application autorisée",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {"type": "string"}
                },
                "required": ["app"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getLocalisation",
            "description": "Retourne la localisation de l'utilisateur",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyseImage",
            "description": "Analyse une image webcam ou screenshot",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "prompt": {"type": "string"},
                    "renew": {"type": "boolean"}
                },
                "required": ["source", "prompt", "renew"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sleepSystem",
            "description": "Met le système en veille",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

# =====================
# UTILITIES
# =====================
def safe_completion(**kwargs):
    tries = 0
    while True:
        try:
            return client.chat.completions.create(**kwargs)
            break
        except APIStatusError:
            tries += 1
            print( f"try {tries}", end="\r" )
            time.sleep(0.5)

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =====================
# TOOL IMPLEMENTATIONS
# =====================
def openLink(link):
    webbrowser.open(link)
    return f"Link opened: {link}"

def openApp(app):
    app = app.lower()
    if app == "spotify":
        os.system("spotify.exe")
    elif app == "teams":
        os.system("ms-teams.exe")
    elif app == "discord":
        pyautogui.typewrite("discord ")
    elif app == "snapchat":
        pyautogui.typewrite("snap ")
    elif app == "vs code":
        pyautogui.typewrite("code ")
    return f"{app} opened"

def getLocalisation():
    try:
        return str(requests.get("https://ipinfo.io/json").json())
    except:
        return "Error getting localisation"

def sleepSystem():
    print("🛑 System sleeping...")
    exit(0)

def capture_image(source):
    if source == "screenshot":
        with mss.mss() as sct:
            for i, monitor in enumerate(sct.monitors[1:], start=1):
                shot = sct.grab(monitor)
                img = Image.frombytes("RGB", shot.size, shot.rgb)
                img.save(os.path.join(SCREENSHOT_DIR, f"screen_{i}.jpg"))
    elif source == "webcam":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite(WEBCAM_PATH, frame)

def analyseImage(source, prompt, renew):
    if renew:
        capture_image(source)

    messages = []

    if source == "screenshot":
        content = [{"type": "text", "text": prompt}]
        for file in sorted(os.listdir(SCREENSHOT_DIR)):
            if file.endswith(".jpg"):
                image_b64 = image_to_base64(os.path.join(SCREENSHOT_DIR, file))
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                })
        messages.append({"role": "user", "content": content})

    elif source == "webcam":
        image_b64 = image_to_base64(WEBCAM_PATH)
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                }
            ]
        })

    response = safe_completion(
        model=VISION_MODEL,
        messages=messages
    )

    return response.choices[0].message.content

# =====================
# MAIN CHAT LOOP
# =====================
def chat():
    print("🤖 RIKA — type 'exit' to quit\n")

    conversation = [
        {
            "role": "system",
            "content": "Tu es un agent logiciel intelligent."
        }
    ]

    while True:
        user_input = input("YOU > ")
        if user_input.lower() == "exit":
            break

        conversation.append({"role": "user", "content": user_input})

        response = safe_completion(
            model=MAIN_MODEL,
            messages=conversation,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message
        conversation.append(message)

        # If tools are called
        if message.tool_calls:
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if name == "openLink":
                    result = openLink(args["link"])
                elif name == "openApp":
                    result = openApp(args["app"])
                elif name == "getLocalisation":
                    result = getLocalisation()
                elif name == "analyseImage":
                    result = analyseImage(
                        args["source"],
                        args["prompt"],
                        args["renew"]
                    )
                elif name == "sleepSystem":
                    sleepSystem()
                else:
                    result = "Unknown tool"

                conversation.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Second call after tool execution
            response = safe_completion(
                model=MAIN_MODEL,
                messages=conversation
            )

            conversation.append(response.choices[0].message)
            print("🤖 >", response.choices[0].message.content)

        else:
            print("🤖 >", message.content)

# =====================
# START
# =====================
if __name__ == "__main__":
    chat()
