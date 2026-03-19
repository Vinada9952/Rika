import pygame
import win32gui
import win32con
import win32api
import pyautogui
import threading


WIDTH = pyautogui.size().width
HEIGHT = pyautogui.size().height

FILL_COLOR = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )

pygame.init()
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( 'Pygame' )
font = pygame.font.Font( None, 36 )
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong( hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong( hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
win32gui.SetLayeredWindowAttributes( hwnd, win32api.RGB( FILL_COLOR[0], FILL_COLOR[1], FILL_COLOR[2] ), 0, win32con.LWA_COLORKEY )

# FIXME: transparency and animation
INITIATING_GIF = pygame.image.load( "./assets/gui/initiating.gif" )

class InitiatingSprite( pygame.sprite.Sprite ):
    def __init__( self ):
        super().__init__()
        self.image = INITIATING_GIF
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

running = True
initiating = False

def startGUI():
    global main_thread
    main_thread.start()

def quitGUI():
    global running
    global main_thread
    running = False
    if main_thread.is_alive():
        main_thread.join()
    pygame.quit()

def setInit( state: bool ):
    global initiating
    initiating = state

all_sprite = pygame.sprite.Group()
initiating_sprite = InitiatingSprite()
all_sprite.add( initiating_sprite )

clock = pygame.time.Clock()

def main():
    global running
    global screen
    global all_sprite
    global clock

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        screen.fill( FILL_COLOR )

        all_sprite.draw( screen )

        pygame.display.flip()
        clock.tick( 30 )

main_thread = threading.Thread( target=main )
main_thread.daemon = True

startGUI()
print( "start GUI" )
import time
time.sleep( 5 )
quitGUI()
print( "quit GUI" )