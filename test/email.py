import smtplib
from email.mime.text import MIMEText
import json

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

settings = Json.read( "./settings.json" )["email"]

def mail( sender, password, receiver, subject, text ):
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

mail(
    settings["email"],
    settings["pwd"],
    settings["contacts"]["William Cote"],
    input( "Sujet\n> " ),
    input( "Message\n> " )
)