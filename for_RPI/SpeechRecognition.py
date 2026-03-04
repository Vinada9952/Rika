# import speech_recognition as sr

# class Sound:

#     def listen( language: str = "fr-FR" ):
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             try:
#                 r.adjust_for_ambient_noise( 1 )
#             except AssertionError:
#                 pass
#             # r.adjust_for_ambient_noise( 1 )
#             audio_data = r.listen( source=source, phrase_time_limit=10 )
#         try:
#             text = r.recognize_google( audio_data, language=language )
#             text = str( text )
#             return text
#         except sr.UnknownValueError:
#             return -1
#         except sr.RequestError:
#             return -2
# print( "you can talk..." )
# while True:
#     print( Sound.listen() )

import speech_recognition as sr

def listen(device_index=5):
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=device_index) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Écoute en cours… (parle maintenant)")
            audio_data = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio_data, language="fr-FR")
    except sr.WaitTimeoutError:
        print("Aucune parole détectée dans le délai imparti")
        return None
    except Exception as e:
        print("Erreur micro :", e)
        return None

if __name__ == "__main__":
    text = listen(device_index=5)
    print("Résultat :", text)