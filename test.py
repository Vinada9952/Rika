# import json
# import requests

# class Json:
#     def write( informations: dict, json_name: str ):
#         json_object = json.dumps( informations, indent=4 )
#         with open( json_name, 'w', encoding="utf-8" ) as outfile:
#             outfile.write( json_object )
#     def read( json_name: str ):
#         with open( json_name, 'r', encoding="utf-8" ) as infile:
#             informations = json.load( infile )
#         return informations

# conversation = Json.read( "./conversation.json" )

# requests.post( "https://rikavinada9952.pythonanywhere.com/setConversation", json=conversation )

from pynput import mouse, keyboard
import threading


def has_user_activity(
    detect_mouse_move: bool = True,
    detect_mouse_click: bool = True,
    detect_mouse_scroll: bool = True,
    detect_keyboard: bool = True,
) -> bool:
    """
    Retourne True si au moins un événement utilisateur s'est produit
    depuis le dernier appel, False sinon.

    Args:
        detect_mouse_move:   Inclure les mouvements souris.
        detect_mouse_click:  Inclure les clics souris.
        detect_mouse_scroll: Inclure le scroll souris.
        detect_keyboard:     Inclure les touches clavier.

    Returns:
        bool: True si une activité correspondante a été détectée.
    """
    detected = threading.Event()

    def _trigger(*_):
        detected.set()

    mouse_listener = mouse.Listener(
        on_move=_trigger if detect_mouse_move else None,
        on_click=_trigger if detect_mouse_click else None,
        on_scroll=_trigger if detect_mouse_scroll else None,
    )
    keyboard_listener = keyboard.Listener(
        on_press=_trigger if detect_keyboard else None,
    )

    mouse_listener.start()
    keyboard_listener.start()

    result = detected.is_set()

    mouse_listener.stop()
    keyboard_listener.stop()

    return result


# ── Exemple d'utilisation ────────────────────────────────────────────────────

from pynput import mouse, keyboard

_detected = threading.Event()

def _trigger(*_):
    _detected.set()

mouse.Listener(on_move=_trigger, on_click=_trigger, on_scroll=_trigger).start()
keyboard.Listener(on_press=_trigger).start()

while True:
    if _detected.is_set():
        print("✔ Activité détectée !")
        _detected.clear()  # reset pour le prochain cycle
    else:
        print("✘ Aucune activité")