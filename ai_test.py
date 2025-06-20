from Vincent import *


class Inputs:
    
    write = ""
    w_f = False
    hear = ""
    h_f = False
    understanding = True


    def _get_input():
        try:
            Inputs.write = input()
            Inputs.w_f = True
        finally:
            pass

    


    def _get_listen():
        hear = ""
        try:

            r = sr.Recognizer()
            while Inputs.w_f:
                try:
                    time.sleep( 0.01 )
                    with sr.Microphone() as source:
                        try:
                            r.adjust_for_ambient_noise( 1 )
                        except AssertionError:
                            pass
                        # r.adjust_for_ambient_noise( 1 )
                        audio_data = r.listen( source )
                    try:
                        hear = r.recognize_google( audio_data, language='fr' )
                        hear = str( hear )
                    except sr.UnknownValueError:
                        hear = -1
                    except sr.RequestError as e:
                        raise sr.RequestError( str( e ) )
                except:
                    pass

            
            if Inputs.understanding and hear == -1:
                Inputs.hear = ""
            elif Type.get_type( hear ) == "str" and hear != "":
                Inputs.hear = hear
            Inputs.h_f = True
        finally:
            pass


    def _anyInputs():

        # if Inputs.understanding == None:
        #     raise Exception( "Static function, please make dynamic object" )

        ret = None


        audio = threading.Thread( target=Inputs._get_listen )
        write = threading.Thread( target=Inputs._get_input )

        audio.start()
        write.start()

        while True:
            print( f"{Inputs.w_f=}" )
            print( f"{Inputs.h_f=}" )
            print( f"{Inputs.write=}" )
            print( f"{Inputs.hear=}\n\n" )
            if Inputs.w_f:
                ret = Inputs.write
                return ret
            if Inputs.h_f:
                ret = Inputs.hear
                return ret

    def input( prompt, understanding ):
        print( prompt )
        if understanding == True or understanding == False:
            Inputs._understanding = understanding
        else:
            raise Exception( f"{understanding=} is not bool" )

        return Inputs._anyInputs()


print( f"this is the input : {Inputs.input( "this is a prompt", True )} done" )