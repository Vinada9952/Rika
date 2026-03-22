import pygame
import win32gui
import win32con
import win32api
import pyautogui
import time
import threading
import cv2
from pynput import mouse, keyboard


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
    win32gui.GetWindowLong( hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED
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
        global display_rika
        display_rika = value
        # print( f"{value=}, {display_rika=}" )
    
    def setTextToDisplay( value ):
        global text
        text = value

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

all_sprite.add( initiating_sprite )
all_sprite.add( loading_sprite )
all_sprite.add( ready_sprite )
all_sprite.add( rika )

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
        

        if int( time.time() ) - last_movement > 15:
            rika.setSize( WIDTH/3, WIDTH/3 )
            rika.setPos( ( WIDTH/3, HEIGHT/5 ) )
            if _detected.is_set():
                last_movement = int( time.time() )
                rika.setPos( ( 20, HEIGHT-WIDTH/10-20 ) )
                _detected.clear()
        else:
            rika.setSize( WIDTH/10, WIDTH/10 )
            if pyautogui.position().x < WIDTH/5 and pyautogui.position().y >= HEIGHT/4*3:
                rika.setPos( ( WIDTH-WIDTH/10-20, HEIGHT-WIDTH/10-20 ) )
            elif pyautogui.position().x > WIDTH/5*4 and pyautogui.position().y >= HEIGHT/4*3:
                rika.setPos( ( 20, HEIGHT-WIDTH/10-20 ) )

        initiating_sprite.update( dt, initiating )
        loading_sprite.update( loaded, initiating )
        rika.update( dt, ready, display_rika )
        ready_sprite.update( dt )

        font_size = max(12, int(36 * rika.current_size[0] / (WIDTH/3)))
        font = pygame.font.Font( "./assets/gui/Nasalization Rg.otf", font_size )
        show_text = font.render( text, True, LIGHT_BLUE )


        screen.fill( FILL_COLOR )
        if ready:
            if rika.rect.x + rika.rect.width / 2 > WIDTH / 2:
                text_pos = (rika.rect.x - show_text.get_width(), rika.rect.y)
            else:
                text_pos = (rika.rect.x + rika.rect.width, rika.rect.y)
            screen.blit( show_text, text_pos )
        all_sprite.draw( screen )
        pygame.display.flip()

        clock.tick( 30 )


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
    GUI.setTextToDisplay( "Hello World" )

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