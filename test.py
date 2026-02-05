import json
from google import genai

# =====================
# INITIALISATION CONVERSATION
# =====================

conversation = [
    {
        "role": "user",
        "parts": [
            {
                "text": "You are an asian parent, like on the media, like Steven He. Your name is AsianGPT and you don't accept failure"
            }
        ]
    }
]

# =====================
# LECTURE CLÉ API
# =====================

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

api_key = data["gemini-api-key"]

# =====================
# CLIENT GEMINI
# =====================

client = genai.Client(api_key=api_key)

# =====================
# PREMIÈRE RÉPONSE
# =====================

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation
)

print("Réponse de AsianGPT :")
print(response.text)

conversation.append(
    {
        "role": "model",
        "parts": [
            {
                "text": response.text
            }
        ]
    }
)

input("\nAppuyez sur Entrée pour continuer...\n")

# =====================
# BOUCLE DE CHAT
# =====================

while True:
    prompt = input("Entrez votre prompt : ")

    if prompt.lower() in ["exit", "quit", "q"]:
        print("Fin de la conversation.")
        break

    conversation.append(
        {
            "role": "user",
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    print("\nRéponse de AsianGPT :")
    print(response.text)

    conversation.append(
        {
            "role": "model",
            "parts": [
                {
                    "text": response.text
                }
            ]
        }
    )
