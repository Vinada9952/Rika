from multiprocessing import process
from pynput import mouse, keyboard
import pygetwindow as gw
import threading
import pyautogui
import win32gui
import win32con
import win32api
import pygame
import socket
import json
import time
import sys
import cv2

charged = 0
def charge():
    global charged
    charged += 1
    print( f"Charged {charged}" )

class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, 'w', encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, 'r', encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations

charge()

WIDTH = pyautogui.size().width
HEIGHT = pyautogui.size().height

print( f"{WIDTH=}, {HEIGHT=}" )

FILL_COLOR = ( 0, 0, 0 )
LIGHT_BLUE = tuple( Json.read( "settings.json" )["gui"]["color"] )
FONT = Json.read( "settings.json" )["gui"]["font"]

pygame.init()
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( 'Rika' )

charge()

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong( 
    hwnd,
    win32con.GWL_EXSTYLE,
    ( 
        win32gui.GetWindowLong( hwnd, win32con.GWL_EXSTYLE )
        | win32con.WS_EX_LAYERED
        | win32con.WS_EX_TOOLWINDOW   # ← cache l'icône de la barre des tâches
    ) & ~win32con.WS_EX_APPWINDOW     # ← retire le style qui force l'apparition
)
win32gui.SetLayeredWindowAttributes( 
    hwnd,
    win32api.RGB( FILL_COLOR[0], FILL_COLOR[1], FILL_COLOR[2] ),
    0,
    win32con.LWA_COLORKEY
)
win32gui.SetWindowPos( 
    hwnd,
    win32con.HWND_TOPMOST,
    0, 0, 0, 0,
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
)

charge()

# def hasUserActivity( 
#     detect_mouse_move: bool = True,
#     detect_mouse_click: bool = True,
#     detect_mouse_scroll: bool = True,
#     detect_keyboard: bool = True,
#  ) -> bool:
#     """
#     Retourne True si au moins un événement utilisateur s'est produit
#     depuis le dernier appel, False sinon.

#     Args:
#         detect_mouse_move:   Inclure les mouvements souris.
#         detect_mouse_click:  Inclure les clics souris.
#         detect_mouse_scroll: Inclure le scroll souris.
#         detect_keyboard:     Inclure les touches clavier.

#     Returns:
#         bool: True si une activité correspondante a été détectée.
#     """
#     detected = threading.Event()

#     def _trigger( *_ ):
#         detected.set()

#     mouse_listener = mouse.Listener( 
#         on_move=_trigger if detect_mouse_move else None,
#         on_click=_trigger if detect_mouse_click else None,
#         on_scroll=_trigger if detect_mouse_scroll else None,
#  )
#     keyboard_listener = keyboard.Listener( 
#         on_press=_trigger if detect_keyboard else None,
#  )

#     mouse_listener.start()
#     keyboard_listener.start()

#     result = detected.is_set()

#     mouse_listener.stop()
#     keyboard_listener.stop()

#     return result

def wrapText( text, font, max_width ):
    """Découpe le texte en lignes selon la largeur max en pixels."""
    if text == -1 or text == -2:
        return [""]
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + ( " " if current_line else "" ) + word
        if font.size( test_line )[0] > max_width:
            if current_line:
                lines.append( current_line )
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append( current_line )

    return lines

def forceTopmost():
    win32gui.SetWindowPos( 
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
)

# def onFocusGained( hwnd, callback ):
#     global running
#     def _watch():
#         global running
#         was_focused = False
#         while running:
#             focused_hwnd = win32gui.GetForegroundWindow()
#             is_focused = ( focused_hwnd == hwnd )
            
#             if is_focused and not was_focused:
#                 if callback is not None:
#                     callback()

#             was_focused = is_focused
#             time.sleep( 0.5 )  # 0.1 → 0.5 pour éviter le spam si aucune fenêtre dispo
    
#     t = threading.Thread( target=_watch, daemon=True )
#     t.start()
#     return t

# def looseFocus():
#     # return
#     other_windows = []
#     def enum_handler( h, _ ):
#         if h != hwnd and win32gui.IsWindowVisible( h ) and win32gui.GetWindowText( h ):
#             other_windows.append( h )
#     win32gui.EnumWindows( enum_handler, None )
    
#     if other_windows:
#         pyautogui.hotkey( 'alt', 'tab' )
#     else:
#         # Minimise plutôt que de crasher
#         win32gui.ShowWindow( hwnd, win32con.SW_MINIMIZE )

charge()

class Loading( pygame.sprite.Sprite ):
    last_image = None
    frame_updated = False
    def __init__( self, file_path ):
        super().__init__()

        self.cap = cv2.VideoCapture( file_path )

        self.frame_number = 0
        self.frame_total = int( self.cap.get( cv2.CAP_PROP_FRAME_COUNT ) )

        if not self.cap.isOpened():
            raise Exception( "Impossible d'ouvrir la vidéo" )

        self.fps = self.cap.get( cv2.CAP_PROP_FPS )
        self.frame_delay = 1000 / self.fps if self.fps > 0 else 33

        # Charger toutes les frames dans un array
        self.frames = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )

            # 🔥 créer un alpha basé sur la luminosité
            gray = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )

            # seuil → ajuste ici ( plus haut = enlève plus de noir )
            _, alpha = cv2.threshold( gray, 25, 255, cv2.THRESH_BINARY )

            # combine RGB + Alpha → RGBA
            frame_rgba = cv2.cvtColor( frame, cv2.COLOR_RGB2RGBA )
            frame_rgba[:, :, 3] = alpha

            # pygame
            surface = pygame.image.frombuffer( 
                frame_rgba.tobytes(),
                frame_rgba.shape[1::-1],
                "RGBA"
            )

            # scale to full width, preserve aspect ratio
            scale_x = WIDTH / surface.get_width()
            
            new_width = WIDTH
            new_height = int( surface.get_height() * scale_x )
            surface = pygame.transform.scale( surface, ( new_width, new_height ) )
            
            # center vertically
            self.frames.append( surface.convert_alpha() )

        self.cap.release()

        self.frame_time = 0
        self.image = self.frames[0] if self.frames else None

        self.rect = pygame.Rect( 0, 0, new_width if self.frames else 0, new_height if self.frames else 0 )

        self.frame_number = 0
        self.last_image = self.image
    
    def readFrame( self ):
        self.frame_number = (self.frame_number + 1) % len(self.frames)
        surface = self.frames[self.frame_number]

        # center vertically
        self.rect.x = 0
        self.rect.y = 0
        self.rect.width = surface.get_width()
        self.rect.height = surface.get_height()

        self.image = surface
        self.last_image = self.image
        self.frame_updated = True
    
    def setToFrame( self, frame_number ):
        if frame_number < 0:
            frame_number = 0
        elif frame_number >= len(self.frames):
            frame_number = len(self.frames) - 1
        self.frame_number = frame_number

    def update( self, dt, initiating: bool ):
        self.frame_updated = False
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time = 0

        # print( f"{initiating=}, {self.frame_number=}, {self.frame_total=}" )
        if initiating:
            if self.frame_number < 230:
                self.frame_number += 1
                if self.frame_number >= len(self.frames):
                    self.frame_number = len(self.frames) - 1
                self.image = self.frames[self.frame_number]
                self.frame_updated = True
        if initiating == False:
            if self.frame_number != 0:
                if self.frame_number < 230:
                    self.frame_number = 230
                self.frame_number += 1
                if self.frame_number >= len(self.frames):
                    self.frame_number = 0
                self.image = self.frames[self.frame_number]
                self.frame_updated = True
        
        if not self.frame_updated:
            self.image = self.last_image

class SystemReady( Loading ):
    def update( self, dt ):
        self.frame_updated = False
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time = 0
        
        if self.frame_number != 0:
            self.frame_number += 1
            if self.frame_number >= len(self.frames):
                self.frame_number = 0
            self.image = self.frames[self.frame_number]
            self.rect.y = HEIGHT/3
            self.frame_updated = True
        if self.frame_number == 50:
            self.setToFrame( 230 )
        
        if not self.frame_updated:
            self.image = self.last_image

class SystemOn( Loading ):
    def update( self, dt ):
        self.frame_updated = False
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time = 0
        
        if self.frame_number != 0:
            self.frame_number += 1
            if self.frame_number >= len(self.frames):
                self.frame_number = 0
            self.image = self.frames[self.frame_number]
            self.image = pygame.transform.scale( self.image, ( self.rect.width/10, self.rect.height/10 ) )
            self.rect.y = HEIGHT-HEIGHT/10
            self.frame_updated = True
        if self.frame_number == 50:
            self.setToFrame( 230 )
        
        if not self.frame_updated:
            self.image = self.last_image

class Rika( pygame.sprite.Sprite ):
    last_image = None
    frame_updated = False
    current_pos = ( 0, 0 )
    current_size = ( 0, 0 )
    target_pos = ( 0, 0 )
    target_size = ( 0, 0 )
    def __init__( self, file_path ):
        super().__init__()

        self.cap = cv2.VideoCapture( file_path )

        self.frame_number = 0
        self.frame_total = int( self.cap.get( cv2.CAP_PROP_FRAME_COUNT ) )

        if not self.cap.isOpened():
            raise Exception( "Impossible d'ouvrir la vidéo" )

        self.fps = self.cap.get( cv2.CAP_PROP_FPS )
        self.frame_delay = 1000 / self.fps if self.fps > 0 else 33

        # Charger toutes les frames dans un array
        self.frames = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )

            # 🔥 créer un alpha basé sur la luminosité
            gray = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )

            # seuil → ajuste ici ( plus haut = enlève plus de noir )
            _, alpha = cv2.threshold( gray, 25, 255, cv2.THRESH_BINARY )

            # combine RGB + Alpha → RGBA
            frame_rgba = cv2.cvtColor( frame, cv2.COLOR_RGB2RGBA )
            frame_rgba[:, :, 3] = alpha

            # pygame
            surface = pygame.image.frombuffer( 
                frame_rgba.tobytes(),
                frame_rgba.shape[1::-1],
                "RGBA"
            )
            
            self.frames.append( surface.convert_alpha() )

        self.cap.release()

        self.frame_time = 0
        self.image = self.frames[0] if self.frames else None

        self.current_pos = ( WIDTH/3, HEIGHT/5 )
        self.current_size = ( WIDTH/3, WIDTH/3 )

        self.rect = pygame.Rect( 0, 0, WIDTH/3, WIDTH/3 )

        self.frame_number = 0
        self.last_image = self.image
    
    def readFrame( self ):
        self.frame_number = (self.frame_number + 1) % len(self.frames)
        surface = self.frames[self.frame_number]

        surface = pygame.transform.scale( surface, ( self.current_size[0], self.current_size[1] ) )
        
        # center vertically
        self.rect.x = self.current_pos[0]
        self.rect.y = self.current_pos[1]
        self.rect.width = self.current_size[0]
        self.rect.height = self.current_size[1]

        self.image = surface
        self.last_image = self.image
        self.frame_updated = True

    def setSize( self, width, height ):
        self.target_size = ( width, height )

    def setPos( self, pos: tuple ):
        self.target_pos = pos
    
    def setToFrame( self, frame_number ):
        if frame_number < 0:
            frame_number = 0
        elif frame_number >= len(self.frames):
            frame_number = len(self.frames) - 1
        self.frame_number = frame_number

    def update( self, dt, ready, display ):
        self.frame_updated = False
        # print( f"{self.current_pos=}, {self.current_size=}" )
        if ready:
            self.current_size = ( 
                self.current_size[0] + ( self.target_size[0]-self.current_size[0] )/10,
                self.current_size[1] + ( self.target_size[1]-self.current_size[1] )/10
            )
            self.current_pos = ( 
                self.current_pos[0] + ( self.target_pos[0]-self.current_pos[0] )/10,
                self.current_pos[1] + ( self.target_pos[1]-self.current_pos[1] )/10
            )
            self.frame_time += dt

            if self.frame_time >= self.frame_delay:
                self.frame_time = 0

            if display == True:
                self.frame_number += 1
                if self.frame_number >= len(self.frames):
                    self.frame_number = 0
                surface = self.frames[self.frame_number]
                surface = pygame.transform.scale( surface, ( self.current_size[0], self.current_size[1] ) )
                self.rect.x = self.current_pos[0]
                self.rect.y = self.current_pos[1]
                self.rect.width = self.current_size[0]
                self.rect.height = self.current_size[1]
                self.image = surface
                self.frame_updated = True
                if self.frame_number == 230:
                    self.setToFrame( 20 )
            if display == False:
                if self.frame_number != 0:
                    self.frame_number += 1
                    if self.frame_number >= len(self.frames):
                        self.frame_number = 0
                    surface = self.frames[self.frame_number]
                    surface = pygame.transform.scale( surface, ( self.current_size[0], self.current_size[1] ) )
                    self.rect.x = self.current_pos[0]
                    self.rect.y = self.current_pos[1]
                    self.rect.width = self.current_size[0]
                    self.rect.height = self.current_size[1]
                    self.image = surface
                    self.frame_updated = True
            
        if not self.frame_updated:
            self.image = self.last_image

charge()

class TextInputSprite(pygame.sprite.Sprite):
    last_image = None
    submitted_text = ""
    input_text = ""
    visible = False
    state = "hidden"

    def __init__(self, pos: tuple, size: tuple):
        super().__init__()

        self.pos  = pos
        self.size = size

        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.rect  = pygame.Rect(pos[0], pos[1], size[0], size[1])

        self._font = pygame.font.Font(FONT, 28)

        self._listener = None
        self._start_listener()
        self.last_image = self.image

    def quit(self):
        if self._listener and self._listener.is_alive():
            self._listener.stop()

    def _start_listener(self):
        def on_press(key):
            if not self.visible:
                return
            try:
                char = key.char
                if char:
                    self.input_text += char
            except AttributeError:
                if key == keyboard.Key.backspace:
                    self.input_text = self.input_text[:-1]
                elif key == keyboard.Key.enter:
                    self.submitted_text = self.input_text
                    self.input_text     = ""
                elif key == keyboard.Key.space:
                    self.input_text += " "

        self._listener = keyboard.Listener(
            on_press = on_press,
            suppress = False
        )
        self._listener.start()

    def _restart_listener(self, suppress: bool):
        shift_held = [False]

        shift_map = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '?', '7': '&', '8': '*', '9': '( ', '0': ' )',
            '-': '_', '=': '+', '/': '\\', ';': ':', '.': '"', ',': '\'',
        }

        def on_press(key):
            if not self.visible:
                return
            if key in (keyboard.Key.shift, keyboard.Key.shift_r):
                shift_held[0] = True
                return
            if key == keyboard.Key.backspace:
                self.input_text = self.input_text[:-1]
            elif key == keyboard.Key.enter:
                self.submitted_text = self.input_text
                self.input_text = ""
            elif key == keyboard.Key.space:
                self.input_text += " "
            else:
                try:
                    char = key.char
                    if char:
                        if shift_held[0]:
                            char = shift_map.get(char, char.upper())
                        self.input_text += char
                except AttributeError:
                    pass

        def on_release(key):
            if key in (keyboard.Key.shift, keyboard.Key.shift_r):
                shift_held[0] = False

        if self._listener and self._listener.is_alive():
            self._listener.stop()

        self._listener = keyboard.Listener(
            on_press   = on_press,
            on_release = on_release,
            suppress   = suppress
        )
        self._listener.start()

    def setVisible(self, value: bool):
        if value and self.state == "hidden":
            self.state      = "idle"
            self.visible    = True
            self.input_text = ""
            self._restart_listener(suppress=True)

        elif not value and self.state == "idle":
            self.state   = "hidden"
            self.visible = False
            self._restart_listener(suppress=False)

    def update(self, dt):
        if self.state == "hidden":
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
            return

        surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)

        cursor  = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        display = self.input_text + cursor
        ty      = int(self.size[1] * 0.75)
        lines   = wrapText(display, self._font, WIDTH / 2)
        for i, line in enumerate(lines):
            rendered = self._font.render(line, True, LIGHT_BLUE)
            tx       = (self.size[0] - rendered.get_width()) // 2
            modifier = rendered.get_height() * i
            surface.blit(rendered, (tx, ty + modifier))

        self.image      = surface
        self.last_image = surface
        self.rect.x     = self.pos[0]
        self.rect.y     = self.pos[1]

    def getText(self):
        if self.submitted_text == "":
            return None
        tmp = self.submitted_text
        self.submitted_text = ""
        return tmp

class LoadingSprite( pygame.sprite.Sprite ):
    full_size = 0
    current_percent = 0
    def __init__( self, full_size: int, pos: tuple ):
        super().__init__()
        self.image = pygame.Surface( ( 0, WIDTH/90 ) )
        self.image.fill( LIGHT_BLUE )
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.full_size = full_size
        self.current_percent = 0

    def update( self, percentage_load: float, initiating ):
        speed = ( percentage_load-self.current_percent )/5
        if not initiating:
            speed = -self.current_percent/4
        
        # if abs( speed ) < 10 and speed != 0:
        #     speed = 10*speed/abs( speed )
        if self.current_percent < 0:
            self.current_percent = 0
        
        self.current_percent += speed
        pixel_on = self.current_percent*self.full_size/100
        self.image = pygame.Surface( ( pixel_on, WIDTH/90 ) )
        self.image.fill( LIGHT_BLUE )

running = True
initiating = False
loaded = 0
ready = False
display_rika = False
last_movement = 0
text = ""
system_display = 0

_detected = threading.Event()

def _trigger( *_ ):
    _detected.set()

def focusWindow():
    return
    print( "focus window" )
    window = gw.getWindowsWithTitle( "Rika" )
    if window:
        win = window[0]
        win.restore()   # si minimisée
        win.activate()  # focus

charge()

mouse.Listener( on_move=_trigger, on_click=_trigger, on_scroll=_trigger ).start()
keyboard.Listener( on_press=_trigger ).start()

client_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
client_socket.connect( ( 'localhost', Json.read( "./settings.json" )["gui"]["communication-port"] ) )

socket_running = True
queue_send = []
to_send = ""

def callFunctionWithArgs( func_name, *args ):
    if func_name in functions:
        functions[func_name]( *args )

def callFunction( func_name ):
    if func_name in functions:
        functions[func_name]()

def send():
    global queue_send, to_send, socket_running
    while socket_running:
        if queue_send:
            input_string = str( queue_send.pop( 0 ) )

            if not input_string.endswith( '\n' ):
                input_string += '\n'

            # Envoi des données
            client_socket.sendall( input_string.encode( 'utf-8' ) )
        else:
            time.sleep( 0.1 )


def onReceiveSocket():
    global socket_running
    while socket_running:
        try:
            received = client_socket.recv( 1024 ).decode( 'utf-8' )
            if received.find( '\n' ) != -1:
                informations = received.split( '\n' )
            else:
                informations = [received]
            for i, information in enumerate( informations ):
                if len( information ) == 0:
                    informations.pop( i )
            for information in informations:
                try:
                    print( information )
                    data = json.loads( information )
                    print( "data received :", json.dumps( data, indent=4 ) )

                    if data["args"] != None:
                        callFunctionWithArgs( data["function"], data["args"] )
                    else:
                        callFunction( data["function"] )
                except json.JSONDecodeError as e:
                    print( e )
        except ConnectionResetError:
            print( "Connection closed by server" )
            socket_running = False
            GUI.quitGUI()


def sendDataSocket( value ):
    global queue_send
    queue_send.append( value )


def quitSocket():
    global socket_running
    socket_running = False

charge()

socket_receive_thread = threading.Thread( target=onReceiveSocket, name="GUI-RX-RIKA" )
socket_send_thread = threading.Thread( target=send, name="GUI-TX-RIKA" )

socket_receive_thread.daemon = True
socket_send_thread.daemon = True

socket_receive_thread.start()
socket_send_thread.start()

charge()

class GUI:
    def startGUI():
        print( "Start GUI" )
        global running
        running = True


    def quitGUI():
        print( "Quit GUI" )
        global running, socket_receive_thread, socket_send_thread
        running = False
        global loading_sprite, initiating_sprite, ready_sprite, rika, text_input_sprite
        text_input_sprite.quit()
        quitSocket()
        while socket_receive_thread.is_alive():
            socket_receive_thread.join()
        while socket_send_thread.is_alive():
            socket_send_thread.join()
        pygame.quit()
        sys.exit()
        exit()
        raise Exception( "Quit GUI" )


    def setInit( state: bool ):
        print( f"Set initiating: {state}" )
        global initiating
        initiating = state

    def setLoading( load ):
        print( f"Set loading: {load}" )
        global loaded
        loaded = load
    
    def displayRika( value ):
        print( f"Set display rika: {value}" )
        global display_rika, last_movement
        display_rika = value
        if display_rika == False:
            GUI.setTextToDisplay( "" )
        last_movement = 0
    
    def setTextToDisplay( value ):
        print( f"Set text to display: {value}" )
        global text
        text = value
    
    def textInput( value: bool ):
        print( f"Set text input visible: {value}" )
        global text_input_sprite
        text_input_sprite.setVisible( value )
    
    def getInput():
        global text_input_sprite
        return text_input_sprite.getText()
    
    def getTextInputState():
        global text_input_sprite
        return text_input_sprite.state

    def forceTopMost():
        forceTopmost()

charge()

functions = {
    "quitGUI": GUI.quitGUI,
    "setInit": GUI.setInit,
    "setLoading": GUI.setLoading,
    "displayRika": GUI.displayRika,
    "setTextToDisplay": GUI.setTextToDisplay,
    "textInput": GUI.textInput,
}

charge()

all_sprite = pygame.sprite.Group()

initiating_sprite = Loading( 
    "./assets/gui/Blender/loading0001-0250.avi"
)
loading_sprite = LoadingSprite( 
    WIDTH/1.95,
    ( WIDTH/4.29, HEIGHT/26 )
)
ready_sprite = SystemReady( 
    "./assets/gui/Blender/ready0001-0250.avi"
)
system_on_sprite = SystemOn( 
    "./assets/gui/Blender/on0001-0250.avi"
)
rika = Rika( 
    "./assets/gui/Blender/Rika0001-0250.avi"
)
text_input_sprite = TextInputSprite(
    ( WIDTH // 4, HEIGHT // 4 ),
    ( WIDTH // 2, HEIGHT // 2 ),
)

charge()

all_sprite.add( initiating_sprite )
all_sprite.add( loading_sprite )
all_sprite.add( ready_sprite )
all_sprite.add( rika )
all_sprite.add( text_input_sprite )
all_sprite.add( system_on_sprite )

clock = pygame.time.Clock()


charge()

current_text = ""
last_text = ""
current_state = ""
last_state = ""

def main():
    global running, initiating, loaded, ready, display_rika, last_movement, text, system_display, current_text, last_text, current_state, last_state
    global rika, loading_sprite, initiating_sprite, ready_sprite, text_input_sprite, system_on_sprite

    while running:
        dt = clock.get_time()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        if loaded == 100 and not ready:
            ready = True
            ready_sprite.setToFrame( 1 )
        
        if text_input_sprite.visible:
            focusWindow()
            last_movement = int( time.time() )
        
        if int( time.time() ) - last_movement > 10:
            system_display = False
            if _detected.is_set():
                last_movement = int( time.time() )
                _detected.clear()
                rika.setPos( ( 20, HEIGHT-WIDTH/7-20 ) )
            else:
                rika.setSize( WIDTH/3, WIDTH/3 )
                rika.setPos( ( WIDTH/3, HEIGHT/5 ) )
        else:
            rika.setSize( WIDTH/7, WIDTH/7 )
            if pyautogui.position().x < WIDTH/7 and pyautogui.position().y >= HEIGHT/4*3:
                rika.setPos( ( WIDTH-WIDTH/7-20, HEIGHT-WIDTH/7-20 ) )
                if not system_display:
                    focusWindow()
                    print( "System on" )
                    system_display = True
                    system_on_sprite.setToFrame( 1 )
            elif pyautogui.position().x > WIDTH/7*4 and pyautogui.position().y >= HEIGHT/4*3:
                rika.setPos( ( 20, HEIGHT-WIDTH/7-20 ) )
                

        rika               .update( dt, ready, display_rika )
        loading_sprite     .update( loaded, initiating )
        initiating_sprite  .update( dt, initiating )
        ready_sprite       .update( dt )
        text_input_sprite  .update( dt )
        system_on_sprite   .update( dt )

        current_text = GUI.getInput()
        current_state = GUI.getTextInputState()

        if current_text != last_text and current_text is not None:
            print( "sending current text" )
            sendDataSocket(
                json.dumps(
                    {
                        "variable": "text_input_text",
                        "value": current_text
                    }
                )
            )
        if current_state != last_state:
            print( "sending current state" )
            sendDataSocket(
                json.dumps(
                    {
                        "variable": "text_input_state",
                        "value": current_state
                    }
                )
            )

        last_text = current_text
        last_state = current_state

        # print( "GUI updated" )

        font_size = max( 12, int( 36 * rika.current_size[0] / ( WIDTH / 3 ) ) )
        font = pygame.font.Font( FONT, font_size )

        max_text_width = rika.current_size[0]
        lines = wrapText( text, font, max_text_width )

        # Calcule la position de base
        if rika.rect.x + rika.rect.width / 2 > WIDTH / 2:
            text_x = rika.rect.x - max_text_width
        else:
            text_x = rika.rect.x + rika.rect.width

        text_y = rika.rect.y

        screen.fill( FILL_COLOR )
        if ready:
            for line in lines:
                rendered = font.render( line, True, LIGHT_BLUE )
                screen.blit( rendered, ( text_x, text_y ) )
                text_y += font.get_linesize()


        all_sprite.draw( screen )
        pygame.display.flip()

        clock.tick( 30 )

charge()

# onFocusGained( hwnd, looseFocus )

# main_thread = threading.Thread( target=main )
# main_thread.daemon = True

GUI.startGUI()
print( "sending ready..." )
time.sleep( 1 )
sendDataSocket(
    json.dumps(
        {
            "variable": "gui_ready",
            "value": True
        }
    )
)
print( "sent!" )
main()