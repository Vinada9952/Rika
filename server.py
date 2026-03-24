from flask import Flask, request


app = Flask(__name__)


conversation = [
    {
        "role": "system",
        "name": "instructions",
        "content": ""
    }
]

@app.route('/setConversation', methods=['POST'])
def setConversation():
    global conversation
    # Use request.get_json() to parse the incoming JSON data
    # It returns a Python dictionary (or None if the content type is incorrect or the body is empty)
    data = request.get_json()

    conversation = data
    return { "status": "succes" }, 200

@app.route( '/getConversation', methods=['GET'] )
def getConversation():
    global conversation
    return conversation