import os
os.system("")  # Enables ANSI escape sequences on Windows

# Colors
RESET = '\033[0m'

for i in range( 100 ):
    print( f'\033[{i}m{i}. Hello World{RESET}' )