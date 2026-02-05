from flask import Flask, request, Response, render_template_string
from groq import Groq
import os
import webbrowser
# import pygame

# pygame.init()

# screen = pygame.display.set_mode( 200, 200 )

# API_KEY = "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"

if os.path.exists( "./GROQ_API.key" ):
    with open( "./GROQ_API.key", "r" ) as f:
        API_KEY = f.read()
else:
    API_KEY = input( "API Key (on https://console.groq.com/keys) : " )
    with open( "./GROQ_API.key", 'x' ) as f:
        f.write( API_KEY )
client = Groq(api_key=API_KEY)
app = Flask(__name__)

conversation = [
    {
        "role": "system",
        "content": "You are an asian parent, like on the media, more like Steven He. Your name is AsianGPT and you don't accept failure. You are very severe, and as soon as something is perfect, it's failure. Rice is the only healthy food. You exagerete everything to make you feel better. For example, When you went to school, you had to go 40 km uphill at 80 degrees, with one foot, other foot was busy starting a business"
    }
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>AsianGPT</title>
    <style>
        body { font-family: Arial; background: #111; color: #eee; padding: 20px; }
        #chat { white-space: pre-wrap; margin-bottom: 20px; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h2>💬 AsianGPT</h2>
    <div id="chat"></div>

    <input id="msg" placeholder="Écris ton message..." />
    <button onclick="send()">Envoyer</button>

    <script>
        function send() {
            const input = document.getElementById("msg");
            const chat = document.getElementById("chat");

            chat.innerHTML += "\\n\\nToi : " + input.value + "\\nIA : ";

            fetch("/chat", {
                method: "POST",
                body: input.value
            }).then(response => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) return;
                        chat.innerHTML += decoder.decode(value);
                        read();
                    });
                }
                read();
            });

            input.value = "";
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.data.decode("utf-8")

    conversation.append({
        "role": "user",
        "content": user_input
    })

    def generate():
        full_response = ""

        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                yield token

        conversation.append({
            "role": "assistant",
            "content": full_response
        })

    return Response(generate(), mimetype="text/plain")

if __name__ == '__main__':
    webbrowser.open( "http://localhost:9952/" )
    app.run( host='127.0.0.1', port=9952 )
