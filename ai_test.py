from groq import Groq

# =========================
# CONFIG
# =========================
API_KEY = "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"

client = Groq(api_key=API_KEY)

conversation = [
    {
        "role": "system",
        "content": "Tu es un assistant utile et amical."
    }
]

print("Chat Groq en streaming (tape 'quit' pour quitter)\n")

while True:
    user_input = input("Toi : ")

    if user_input.lower() in ["quit", "exit"]:
        break

    conversation.append({
        "role": "user",
        "content": user_input
    })

    print("IA : ", end="", flush=True)

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation,
        stream=True
    )

    full_response = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            print(token, end="", flush=True)
            full_response += token

    print("\n")

    conversation.append({
        "role": "assistant",
        "content": full_response
    })
