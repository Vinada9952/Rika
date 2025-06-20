bar_count = 0

def loadBar( total ):
    global bar_count
    bar_count += 1

    bar = "[" + ( '.'*100 ) + "]"


    for i in range( int( bar_count*100/total ) ):
        bar = bar.replace( ".", "#", 1 )

    print( bar, f"{bar_count}/{total}", end='\r' )
    if bar == total:
        print( "\n" )

import time
for i in range( 100 ):
    time.sleep( 0.01 )
    loadBar( 100 )