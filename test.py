"""
Reconnaissance vocale TEMPS RÉEL avec SpeechRecognition
Gratuit (API Google publique)
Nécessite connexion Internet
"""

import speech_recognition as sr
import threading
import sys

# =====================
# CONFIG
# =====================

LANGUAGE = "fr-FR"  # Change si nécessaire

# =====================
# INITIALISATION
# =====================

recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("=" * 60)
print("🎤 RECONNAISSANCE VOCALE TEMPS RÉEL")
print("=" * 60)
print("Langue :", LANGUAGE)
print("Parlez... (Ctrl+C pour quitter)\n")

# Ajustement au bruit ambiant
with microphone as source:
    print("🔧 Ajustement au bruit ambiant...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("✅ Prêt !\n")

# =====================
# CALLBACK
# =====================

def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language=LANGUAGE)
        print("📝", text)

    except sr.UnknownValueError:
        # Rien compris → on ignore silencieusement
        pass

    except sr.RequestError as e:
        print("❌ Erreur API Google :", e)

# =====================
# LANCEMENT ECOUTE CONTINUE
# =====================

stop_listening = recognizer.listen_in_background(
    microphone,
    callback,
    phrase_time_limit=5  # Durée max d'une phrase
)

# Boucle principale
try:
    while True:
        pass

except KeyboardInterrupt:
    print("\n👋 Arrêt du programme")
    stop_listening(wait_for_stop=False)
    sys.exit()
