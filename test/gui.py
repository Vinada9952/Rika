import pygame
import win32gui
import win32con
import win32api
import pyautogui
import threading
import cv2


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
    
    def getReady( self ):
        if self.frame_number < 20:
            return False
        return True

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
        speed = (percentage_load-self.current_percent)/10
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

all_sprite = pygame.sprite.Group()

initiating_sprite = Loading(
    "./assets/gui/Blender/loading0001-0250.avi"
)
loading_sprite = LoadingSprite(
    WIDTH/1.93,
    ( WIDTH/4.29, HEIGHT/26 )
)

all_sprite.add( initiating_sprite )
all_sprite.add( loading_sprite )

clock = pygame.time.Clock()


def main():
    global running, initiating, loaded

    while running:
        dt = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        initiating_sprite.update( dt, initiating )
        loading_sprite.update( loaded, initiating )

        screen.fill( FILL_COLOR )
        all_sprite.draw( screen )
        pygame.display.flip()

        clock.tick( 30 )


main_thread = threading.Thread( target=main )
main_thread.daemon = True


import time

print( "start" )
startGUI()
time.sleep( 1 )

print( "init true" )
setInit( True )
time.sleep( 1 )

print( "Loading" )
for i in range( 50 ):
    setLoading( i )
    time.sleep( 0.01 )
time.sleep( 1 )
for i in range( 20 ):
    setLoading( 80+i )
    time.sleep( 0.1 )
time.sleep( 5 )

print( "init false" )
setInit( False )
time.sleep( 5 )

print( "quit" )
quitGUI()