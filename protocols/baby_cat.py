from email.mime.text import MIMEText
import smtplib

def sendEmail( receiver: str, subject: str, text: str ):
    msg = MIMEText( text )
    msg["Subject"] = subject
    msg["From"] = "Rika.Vinada9952@gmail.com"
    msg["To"] = receiver

    # print( f"{receiver=}, {subject=}, {text=}" )

    with smtplib.SMTP( "smtp.gmail.com", 587 ) as server:
        server.starttls()
        server.login( "Rika.Vinada9952@gmail.com", "ywbn pcia fyzx hmfz" )
        server.sendmail( "Rika.Vinada9952@gmail.com", receiver, msg.as_string() )
    
    return "Envoie du courriel réussi", False

sendEmail( "mariannelord@icloud.com", "Protocol Bébé Chat", "https://ca.pinterest.com/vinada9952/pour-marianne/\n\nMiaou" )