# 🤖 Rika — Assistant IA avec Interface Graphique

Rika est un assistant intelligent en Python combinant :
- 🎤 Reconnaissance vocale (SpeechRecognition + Whisper)
- 🧠 Modèles IA (Groq, Ollama)
- 🖥️ Interface graphique temps réel (Pygame + transparence Windows)
- 🔊 Synthèse vocale (Edge TTS)
- 🎵 Intégration Spotify
- 📡 Communication GUI ↔ Core via sockets

---

## ⚙️ INSTALLATION

- Pour installer, exécuter le script `setup.py`
- Pour lancer, lancer `Rika.py` pour utiliser l'assistant

### Setup automatique

Le script `setup.py` :
- Crée les dossiers nécessaires (`cache`, `assets`, etc.)
- Génère les fichiers de base :
  - protocols.json
  - contacts.json
  - playlists.json
  - usernote.txt
- Configure :
  - clé API Groq
  - utilisateur
  - email (optionnel)
  - Spotify (optionnel)
  - nom de l’assistant + calibration vocale

---

## ✨ FONCTIONNALITÉS

- Obtenir la localisation
- Avoir l'heure, date, etc.
- Avoir la météo de votre localisation
- Capture automatique de l'écran et analyse (à votre demande)
- Capture automatique de la webcam et analyse (à votre demande)
- Ouvrir une application installée sur l'ordinateur
- Ouvrir un lien web
- Recherche sur le web
- Envoyer un courriel
- Lire des courriels
- Exécuter des actions custom via des protocols (`protocols.json`)
- Sauvegarder un fichier
- Reconnaître une musique
- Jouer de la musique sur Spotify
- Créer des diagrammes

---

## 🖥️ INTERFACE GRAPHIQUE

- Overlay transparent always-on-top
- Animations vidéo (OpenCV → Pygame)
- Affichage dynamique (chargement, état, assistant)
- Input texte intégré

---

## 🎤 UTILISATION

- Pour lui parler :
  - Dire son nom (par défaut : **Rika**)
  - Ou utiliser le raccourci clavier (par défaut : `ctrl + alt + r`)
- Pour arrêter :
  - Dire "au revoir"
  - Ou demander la mise en veille

⚠️ NOTE :
L'input clavier ne fonctionne pas dans d'autres applications si le mode conversation est actif

---

## ⚙️ OPTIONS

- Modifier les paramètres dans `settings.json`
- Personnaliser l’overlay via les assets
- Modifier :
  - voix
  - modèles IA
  - raccourcis clavier
  - couleur GUI
  - volume audio

---

## 🧩 ARCHITECTURE

- `Rika.py` → logique principale (IA, audio, API)
- `gui.py` → affichage graphique
- Communication via socket TCP (localhost)
- Multithreading intensif

### Pipeline vocal

Micro → SpeechRecognition  
        ↓  
     (si OK)  
        ↓  
    Whisper (async)  
        ↓  
Fusion LLM (Groq)  
        ↓  
Commande finale  

---

## 📁 STRUCTURE

.
├── Rika.py  
├── gui.py  
├── setup.py  
├── settings.json  
├── conversation.json  
├── log.json  
├── cache/  
│   ├── output.mp3  
│   ├── screenshots/  
│   └── webcam/  
└── assets/  

---

## 🔌 INTÉGRATIONS

- Spotify API
- Email (SMTP / IMAP)
- Shazam (reconnaissance musique)
- Web requests
- Ollama (local)
- Groq (cloud)

---

## ⚠️ LIMITATIONS

- Windows recommandé (transparence GUI)
- Dépend de services externes (API)
- Whisper peut être lent sans GPU
- Multithreading complexe

---

## 🔒 SÉCURITÉ

- Les clés API sont stockées localement (`settings.json`)
- Aucune sandbox → attention aux commandes exécutées

---

## 🛠️ TROUBLESHOOTING

- Envoyer les fichiers :
  - `log.json`
  - `debug.json` (si présent)
- Optionnel :
  - `conversation.json` (historique)

Avec :
- Description du bug
- Étapes pour reproduire

---

## 🧠 AUTEUR

Développé par Vincent Tuê Minh Boucher