from Vincent import GoogleHome


home = GoogleHome()


home.print_devices()
home.send_msg( "Bonjour, c'est Vincent qui parle ici", home.choose_device( input() ) )