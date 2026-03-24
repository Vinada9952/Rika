import pygame
import win32gui
import win32con
import win32api
import pyautogui
import time
import threading
import cv2
from pynput import mouse, keyboard
import ctypes
from ctypes import wintypes


WIDTH = pyautogui.size().width
HEIGHT = pyautogui.size().height

print( f"{WIDTH=}, {HEIGHT=}" )

FILL_COLOR = ( 0, 0, 0 )
LIGHT_BLUE = ( 3, 232, 252 )

pygame.init()
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( 'Pygame' )


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

def wrap_text(text, font, max_width):
    """Découpe le texte en lignes selon la largeur max en pixels."""
    if text == -1 or text == -2:
        return [""]
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] > max_width:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    return lines

def onFocusGained(hwnd, callback):
    """
    Appelle callback() quand la fenêtre hwnd gagne le focus.
    Lance un thread de surveillance en arrière-plan.
    """
    def _watch():
        was_focused = False
        while True:
            focused_hwnd = win32gui.GetForegroundWindow()
            is_focused = (focused_hwnd == hwnd)
            
            if is_focused and not was_focused:
                if callback is not None:
                    callback()

            
            was_focused = is_focused
            time.sleep(0.1)
    
    t = threading.Thread(target=_watch, daemon=True)
    t.start()
    return t

def looseFocus():
    pyautogui.hotkey('alt', 'tab')


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

        self.frame_time = 0
        self.image = None

        self.rect = pygame.Rect( 0, 0, WIDTH, HEIGHT )

        self.readFrame()
        self.frame_number = 0
    
    def readFrame( self ):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.set( cv2.CAP_PROP_POS_FRAMES, 0 )
            ret, frame = self.cap.read()
        self.frame_number = int( self.cap.get( cv2.CAP_PROP_POS_FRAMES ) ) - 1

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
        new_height = int(surface.get_height() * scale_x)
        surface = pygame.transform.scale(surface, (new_width, new_height))
        
        # center vertically
        self.rect.x = 0
        self.rect.y = 0
        self.rect.width = new_width
        self.rect.height = new_height

        self.image = surface.convert_alpha()
        self.last_image = self.image
        self.frame_updated = True
    
    def setToFrame( self, frame_number ):
        if frame_number < 0:
            frame_number = 0
        elif frame_number >= self.frame_total:
            frame_number = self.frame_total - 1
        self.cap.set( cv2.CAP_PROP_POS_FRAMES, frame_number )
        self.frame_number = frame_number

    def update( self, dt, initiating: bool ):
        self.frame_updated = False
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time = 0

        # print( f"{initiating=}, {self.frame_number=}, {self.frame_total=}" )
        if initiating == True:
            if self.frame_number != 230:
                self.readFrame()
        if initiating == False:
            if self.frame_number != 0:
                if self.frame_number < 230:
                    self.setToFrame( 230 )
                self.readFrame()
        
        if not self.frame_updated:
            self.image = self.last_image

class SystemReady( Loading ):
    def update( self, dt ):
        self.frame_updated = False
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time = 0
        
        if self.frame_number != 0:
            self.readFrame()
            self.rect.y = HEIGHT/3
        if self.frame_number == 50:
            self.setToFrame( 230 )
        
        if not self.frame_updated:
            self.image = self.last_image

class Rika( pygame.sprite.Sprite ):
    last_image = None
    frame_updated = False
    current_pos = (0, 0)
    current_size = (0, 0)
    target_pos = (0, 0)
    target_size = (0, 0)
    def __init__( self, file_path ):
        super().__init__()

        self.cap = cv2.VideoCapture( file_path )

        self.frame_number = 0
        self.frame_total = int( self.cap.get( cv2.CAP_PROP_FRAME_COUNT ) )

        if not self.cap.isOpened():
            raise Exception( "Impossible d'ouvrir la vidéo" )

        self.fps = self.cap.get( cv2.CAP_PROP_FPS )
        self.frame_delay = 1000 / self.fps if self.fps > 0 else 33

        self.frame_time = 0
        self.image = None

        self.current_pos = ( WIDTH/3, HEIGHT/5 )
        self.current_size = ( WIDTH/3, WIDTH/3 )

        self.rect = pygame.Rect( 0, 0, WIDTH/3, WIDTH/3 )

        self.readFrame()
        self.frame_number = 0
    
    def readFrame( self ):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.set( cv2.CAP_PROP_POS_FRAMES, 0 )
            ret, frame = self.cap.read()
        self.frame_number = int( self.cap.get( cv2.CAP_PROP_POS_FRAMES ) ) - 1

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
        
        surface = pygame.transform.scale(surface, (self.current_size[0], self.current_size[1]))
        
        # center vertically
        self.rect.x = self.current_pos[0]
        self.rect.y = self.current_pos[1]
        self.rect.width = self.current_size[0]
        self.rect.height = self.current_size[1]

        self.image = surface.convert_alpha()
        self.last_image = self.image
        self.frame_updated = True

    def setSize(self, width, height):
        self.target_size = ( width, height )

    def setPos( self, pos: tuple ):
        self.target_pos = pos
    
    def setToFrame( self, frame_number ):
        if frame_number < 0:
            frame_number = 0
        elif frame_number >= self.frame_total:
            frame_number = self.frame_total - 1
        self.cap.set( cv2.CAP_PROP_POS_FRAMES, frame_number )
        self.frame_number = frame_number

    def update( self, dt, ready, display ):
        self.frame_updated = False
        # print( f"{self.current_pos=}, {self.current_size=}" )
        if ready:
            self.current_size = (
                self.current_size[0] + (self.target_size[0]-self.current_size[0])/10,
                self.current_size[1] + (self.target_size[1]-self.current_size[1])/10
            )
            self.current_pos = (
                self.current_pos[0] + (self.target_pos[0]-self.current_pos[0])/10,
                self.current_pos[1] + (self.target_pos[1]-self.current_pos[1])/10
            )
            self.frame_time += dt

            if self.frame_time >= self.frame_delay:
                self.frame_time = 0

            if display == True:
                self.readFrame()
                if self.frame_number == 230:
                    self.setToFrame( 20 )
            if display == False:
                if self.frame_number != 0:
                    self.readFrame()
            
        if not self.frame_updated:
            self.image = self.last_image

class TextInputSprite( pygame.sprite.Sprite ):
    last_image = None
    frame_updated = False
    submitted_text = ""
    input_text = ""
    visible = False
    state = "hidden"

    def __init__( self, appear_path, idle_path, disappear_path, pos: tuple, size: tuple ):
        super().__init__()

        self.cap_appear    = cv2.VideoCapture( appear_path )
        self.cap_idle      = cv2.VideoCapture( idle_path )
        self.cap_disappear = cv2.VideoCapture( disappear_path )

        self.pos  = pos
        self.size = size

        self.fps         = self.cap_appear.get( cv2.CAP_PROP_FPS ) or 30
        self.frame_delay = 1000 / self.fps
        self.frame_time  = 0

        self.image = pygame.Surface( ( 0, 0 ), pygame.SRCALPHA )
        self.rect  = pygame.Rect( pos[0], pos[1], size[0], size[1] )

        self._font = pygame.font.Font( "./assets/gui/Nasalization Rg.otf", 28 )

        self._listener = None
        self._start_listener()

    # ── listener pynput permanent ─────────────────────────────────────────
    def _start_listener( self ):
        def on_press( key ):
            if not self.visible:
                return  # on laisse passer les touches normalement

            # intercept : supprime le caractère sur la fenêtre en focus
            # en simulant un backspace AVANT que la touche arrive à destination
            # → on supprime la frappe dans la fenêtre cible avec suppress=True
            # (voir Listener(suppress=True) plus bas)

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

        # suppress=True bloque la touche pour toutes les autres fenêtres
        # quand le popup est visible, le listener est recréé avec/sans suppress
        self._listener = keyboard.Listener(
            on_press  = on_press,
            suppress  = False   # sera géré dynamiquement via setVisible
        )
        self._listener.start()

    # def _restart_listener( self, suppress: bool ):
    #     """Recrée le listener avec suppress=True ou False selon visibilité."""
    #     if self._listener and self._listener.is_alive():
    #         self._listener.stop()

    #     def on_press( key ):
    #         if not self.visible:
    #             return

    #         try:
    #             char = key.char
    #             if char:
    #                 self.input_text += char
    #         except AttributeError:
    #             if key == keyboard.Key.backspace:
    #                 self.input_text = self.input_text[:-1]
    #             elif key == keyboard.Key.enter:
    #                 self.submitted_text = self.input_text
    #                 self.input_text     = ""
    #             elif key == keyboard.Key.space:
    #                 self.input_text += " "

    #     self._listener = keyboard.Listener(
    #         on_press = on_press,
    #         suppress = suppress
    #     )
    #     self._listener.start()

    def _restart_listener( self, suppress: bool ):
        shift_held = [False]  # liste pour pouvoir modifier dans le closure

        shift_map = {
            '1': '!',
            '2': '@',
            '3': '#',
            '4': '$',
            '5': '%',
            '6': '?',
            '7': '&',
            '8': '*',
            '9': '(',
            '0': ')',
            '-': '_',
            '=': '+',
            '/': '\\',
            ';': ':',
            ".": '"',
            ',': '\'',
        }

        def on_press( key ):
            if not self.visible:
                return

            # Détecter Shift
            if key in ( keyboard.Key.shift, keyboard.Key.shift_r ):
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
                            if char in shift_map:
                                char = shift_map[char]
                            else:
                                char = char.upper()
                        self.input_text += char
                except AttributeError:
                    pass

        def on_release( key ):
            if key in ( keyboard.Key.shift, keyboard.Key.shift_r ):
                shift_held[0] = False

        if self._listener and self._listener.is_alive():
            self._listener.stop()

        self._listener = keyboard.Listener(
            on_press   = on_press,
            on_release = on_release,
            suppress   = suppress
        )
        self._listener.start()

    # ── méthode publique appelée par GUI ──────────────────────────────────
    def setVisible( self, value: bool ):
        if value and self.state == "hidden":
            self.cap_appear.set( cv2.CAP_PROP_POS_FRAMES, 0 )
            self.state      = "appearing"
            self.visible    = True
            self.input_text = ""
            self._restart_listener( suppress=True )   # bloque les touches

        elif not value and self.state in ( "appearing", "idle" ):
            self.cap_disappear.set( cv2.CAP_PROP_POS_FRAMES, 0 )
            self.state   = "disappearing"
            self.visible = False
            self._restart_listener( suppress=False )  # laisse passer les touches

    # ── lecture frame ─────────────────────────────────────────────────────
    def _read_frame( self, cap, loop=False ):
        ret, frame = cap.read()
        if not ret:
            if loop:
                cap.set( cv2.CAP_PROP_POS_FRAMES, 0 )
                ret, frame = cap.read()
            else:
                return None

        frame      = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )
        gray       = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
        _, alpha   = cv2.threshold( gray, 25, 255, cv2.THRESH_BINARY )
        frame_rgba = cv2.cvtColor( frame, cv2.COLOR_RGB2RGBA )
        frame_rgba[:, :, 3] = alpha

        surface = pygame.image.frombuffer(
            frame_rgba.tobytes(),
            frame_rgba.shape[1::-1],
            "RGBA"
        )
        surface = pygame.transform.scale( surface, ( int(self.size[0]), int(self.size[1]) ) )
        return surface.convert_alpha()

    # ── update ────────────────────────────────────────────────────────────
    def update( self, dt ):
        if self.state == "hidden":
            return

        self.frame_time += dt
        if self.frame_time < self.frame_delay:
            if self.last_image:
                self.image = self.last_image
            return
        self.frame_time = 0

        if self.state == "appearing":
            frame = self._read_frame( self.cap_appear, loop=False )
            if frame is None:
                self.cap_idle.set( cv2.CAP_PROP_POS_FRAMES, 0 )
                self.state = "idle"
                frame = self._read_frame( self.cap_idle, loop=True )

        elif self.state == "idle":
            frame = self._read_frame( self.cap_idle, loop=True )

        elif self.state == "disappearing":
            frame = self._read_frame( self.cap_disappear, loop=False )
            if frame is None:
                self.state      = "hidden"
                self.visible    = False
                self.image      = pygame.Surface( (0, 0), pygame.SRCALPHA )
                self.last_image = self.image
                return

        if frame is not None:
            surface  = frame.copy()
            cursor   = "|" if ( pygame.time.get_ticks() // 500 ) % 2 == 0 else ""
            display  = self.input_text + cursor
            rendered = self._font.render( display, True, LIGHT_BLUE )
            tx = ( self.size[0] - rendered.get_width()  ) // 2
            ty = int( self.size[1] * 0.75 )
            surface.blit( rendered, ( tx, ty ) )
            self.image      = surface
            self.last_image = surface

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def getText( self ):
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

    def update( self, percentage_load: float, initiating ):
        speed = (percentage_load-self.current_percent)/5
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

_detected = threading.Event()

def _trigger(*_):
    _detected.set()



mouse.Listener(on_move=_trigger, on_click=_trigger, on_scroll=_trigger).start()
keyboard.Listener(on_press=_trigger).start()

class GUI:
    def startGUI():
        global main_thread
        main_thread.start()


    def quitGUI():
        global running
        running = False
        if main_thread.is_alive():
            main_thread.join()
        pygame.quit()


    def setInit( state: bool ):
        global initiating
        initiating = state

    def setLoading( load ):
        global loaded
        loaded = load
    
    def displayRika( value ):
        global display_rika, last_movement
        display_rika = value
        if display_rika == False:
            GUI.setTextToDisplay( "" )
        last_movement = 0
    
    def setTextToDisplay( value ):
        global text
        text = value
    
    def textInput( value: bool ):
        global text_input_sprite
        text_input_sprite.setVisible( value )
    
    def getInput():
        global text_input_sprite
        return text_input_sprite.getText()
    
    def getTextInputState():
        global text_input_sprite
        return text_input_sprite.state

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
rika = Rika(
    "./assets/gui/Blender/Rika0001-0250.avi"
)
text_input_sprite = TextInputSprite(
    "./assets/gui/Blender/text_input0001-0005.avi",
    "./assets/gui/Blender/text_input0001-0005.avi",
    "./assets/gui/Blender/text_input0001-0005.avi",
    ( WIDTH // 4, HEIGHT // 4 ),
    ( WIDTH // 2, HEIGHT // 2 ),
)

all_sprite.add( initiating_sprite )
all_sprite.add( loading_sprite )
all_sprite.add( ready_sprite )
all_sprite.add( rika )
all_sprite.add( text_input_sprite )

clock = pygame.time.Clock()


def main():
    global running, initiating, loaded, ready, display_rika, last_movement, text

    while running:
        dt = clock.get_time()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        if loaded == 100 and ready == False:
            ready = True
            ready_sprite.setToFrame( 1 )
        
        if text_input_sprite.visible:
            last_movement = int( time.time() )
        if int( time.time() ) - last_movement > 10:
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
            elif pyautogui.position().x > WIDTH/7*4 and pyautogui.position().y >= HEIGHT/4*3:
                rika.setPos( ( 20, HEIGHT-WIDTH/7-20 ) )

        rika             .update( dt, ready, display_rika )
        loading_sprite   .update( loaded, initiating )
        initiating_sprite.update( dt, initiating )
        ready_sprite     .update( dt )
        text_input_sprite.update( dt )

        font_size = max(12, int(36 * rika.current_size[0] / (WIDTH / 3)))
        font = pygame.font.Font("./assets/gui/Nasalization Rg.otf", font_size)

        max_text_width = rika.current_size[0]
        lines = wrap_text(text, font, max_text_width)

        # Calcule la position de base
        if rika.rect.x + rika.rect.width / 2 > WIDTH / 2:
            text_x = rika.rect.x - max_text_width
        else:
            text_x = rika.rect.x + rika.rect.width

        text_y = rika.rect.y

        screen.fill( FILL_COLOR )
        if ready:
            for line in lines:
                rendered = font.render(line, True, LIGHT_BLUE)
                screen.blit(rendered, (text_x, text_y))
                text_y += font.get_linesize()


        all_sprite.draw( screen )
        pygame.display.flip()

        clock.tick( 30 )

onFocusGained( hwnd, looseFocus() )

main_thread = threading.Thread( target=main )
main_thread.daemon = True


def test():
    print( "start" )
    GUI.startGUI()
    time.sleep( 1 )

    print( "init true" )
    GUI.setInit( True )
    time.sleep( 1 )

    print( "Loading" )
    GUI.setLoading( 100 )
    time.sleep( 2 )

    print( "init false" )
    GUI.setInit( False )
    time.sleep( 5 )

    print( "display Rika" )
    GUI.displayRika( True )
    time.sleep( 5 )

    print( "text display" )
    GUI.setTextToDisplay( "Hello World, this is a test text for Rika GUI text display" )
    time.sleep( 5 )

    GUI.textInput( True )
    while True:
        time.sleep( 0.5 )
        text = GUI.getInput()
        if text:
            print( text )
            break
    GUI.textInput( False )

    try:
        while True:
            time.sleep( 100 )
    except KeyboardInterrupt:
        pass

    print( "remove Rika" )
    GUI.displayRika( False )
    time.sleep( 15 )

    print( "quit" )
    GUI.quitGUI()

test()