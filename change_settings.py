import speech_recognition as sr
import json
import webbrowser

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

def listen( language: str = "fr-FR" ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise( 1 )
            except AssertionError:
                pass
            # r.adjust_for_ambient_noise( 1 )
            audio_data = r.listen( source=source, phrase_time_limit=10 )
        try:
            text = r.recognize_google( audio_data, language=language )
            text = str( text )
            return text
        except sr.UnknownValueError:
            return -1
        except sr.RequestError:
            return -2

settings = Json.read( "./settings.json" )

while True:
    print( "Quel paramètre voulez vous changer ?" )
    print( "1. Nom de l'agent" )
    print( "2. Email de l'agent" )
    print( "3. Clés API" )
    print( "4. Changer la voix" )
    print( "5. Quitter" )
    choice = input( "> " )

    if choice == '1':
        assistant_name = input( "Nom de l'agent : " )
        call_names = []
        calibration = 0
        while True:
            print( "Dites le nom de l'agent dans votre microphone..." )
            listen = listen()
            print( "patientez..." )
            if listen not in call_names:
                call_names.append( listen )
            else:
                calibration += 1
            if calibration == 5:
                break
        settings["calls"]["names"] = call_names
        settings["assistant-name"] = assistant_name
    elif choice == '2':
        settings["email"]["email"] = input( "Email de L'agent : " )
        settings["email"]["pwd"] = input( "Mot de passe de l'agent pour l'email (https://myaccount.google.com/apppasswords)" )
    elif choice == '3':
        qtt = int( input( "Nombre de clés API : " ) )
        for i in range( qtt ):
            settings["api-keys"].append( input( f"Clé #{i+1} : " ) )
    elif choice == '4':
        webbrowser.open( "https://tts.travisvn.com" )
        settings["audio"]["voice"] = input( "Nouvelle voix : " )
    elif choice == '5':
        break
    else:
        print( "choix non accepté" )

Json.write( settings, "./settings.json" )