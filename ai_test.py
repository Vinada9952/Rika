import os
import datetime
import shutil

filename = "captured_image.png"

def moment():
    date = datetime.datetime.now()
    day_name = int( date.strftime( "%w" ) )
    if day_name == 0:
        day_name = "Dimanche"
    elif day_name == 1:
        day_name = "Lundi"
    elif day_name == 2:
        day_name = "Mardi"
    elif day_name == 3:
        day_name = "Mercredi"
    elif day_name == 4:
        day_name = "Jeudi"
    elif day_name == 5:
        day_name = "Vendredi"
    elif day_name == 6:
        day_name = "Samedi"
    jour = date.strftime( "%d" )
    mois = int( date.strftime( "%m" ) )
    if mois == 1:
        mois = "Janvier"
    elif mois == 2:
        mois = "Février"
    elif mois == 3:
        mois = "Mars"
    elif mois == 4:
        mois = "Avril"
    elif mois == 5:
        mois = "Mai"
    elif mois == 6:
        mois = "Juin"
    elif mois == 7:
        mois = "Juillet"
    elif mois == 8:
        mois = "Août"
    elif mois == 9:
        mois = "Septembre"
    elif mois == 10:
        mois = "Octobre"
    elif mois == 11:
        mois = "Novembre"
    elif mois == 12:
        mois = "Décembre"
    ans = date.strftime( "%Y" )
    heure = datetime.datetime.now().strftime( "%H" )
    minute = datetime.datetime.now().strftime( "%M" )
    return str( f"{ans=} {mois=} {jour=} {heure=} {minute=}" )

print( f"./{filename} ./visual-memory/{moment().replace( ' ', '_' )}.png" )
shutil.copyfile( f"./{filename}", f"./visual-memory/{moment().replace( ' ', '_' )}.png" )