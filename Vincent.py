import os
import time
import subprocess
from PIL import Image
import json
import ollama
import datetime
import random
import pychromecast
import math
import serial
import threading
import speech_recognition as sr
import pygame
import pyttsx3
import socket
from ollama import web_fetch, web_search
import socketserver

class Time:
    milliseconde = 1
    centiseconde = 10*milliseconde
    deciseconde = 10*centiseconde
    seconde = 10*deciseconde
    minute = 60*seconde
    heure = 60*minute
    jour = 24*heure
    semaine = 7*jour
    def wait( delay ):
        time.sleep( delay/1000 )

class Serial:
    port = "COM1"
    baud = 9600
    _ser = None
    def __init__( self, port: str, baud: int = 9600 ):
        self.port = port
        self.baud = baud
        self._ser = serial.Serial( self.port )
    
    def send( self, msg, mode ):
        if mode == "chr" or mode == "str" or mode == str or mode == chr:
            self._ser.write( str( msg ).encode() )
        elif mode == "int" or mode == "nbr" or mode == int:
            self._ser.write( chr( msg ).encode() )
        elif mode == "bytes" or mode == bytes:
            self._ser.write( msg )
    
    def getBuffer( self ):
        return self._ser.in_waiting

    def receive( self, mode ):
        recv = self._ser.readline()
        if mode == "chr" or mode == "str" or mode == str or mode == chr:
            return chr( int( recv ) )
        elif mode == "int" or mode == "nbr" or mode == int:
            return int( recv )
        elif mode == "bytes" or mode == bytes:
            return recv
        


WHITE = ( 255, 255, 255 )
GREY = ( 128, 128, 128 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )


class Type:
    def getType( var ):
        try:
            if var == list( var ):
                return "list"
            elif var == str( var ):
                return "str"
        except TypeError:
            try:
                if var == int( var ):
                    return "int"
                elif var == float( var ):
                    return "float"
                elif var == bool( var ):
                    return "bool"
                else:
                    return "Unknown type"
            except TypeError:
                try:
                    if var.keys():
                        return "json"
                except AttributeError:
                    return "Unknown type"
                except TypeError:
                    return "Unknown type"
    class file:
        append = 'a'
        trunc = 'w'
        read = 'r'
        create = 'x'
    def list_cut( origin: str, separator: str ):
        traitement = ""
        origin = origin+separator
        output = []
        for i in range( len( origin ) ):
            if origin[i] == separator:
                output.append( traitement )
                traitement = ""
            else:
                traitement += origin[i]
        return output






class User:
    def input( type ):
        if type == int:
            return int( input() )
        elif type == str:
            return input()
    class print:
        def computer( output, endl: bool, delay: int ):
            output = str( output )
            for i in range( len( output ) ):
                print( output[i], end="" )
                Time.wait( delay )
            if endl == 1:
                print( '\n', end="" )
        def classic( output, endl: bool ):
            if endl == 1:
                output += '\n'
            print( output, end='' )
        def array( output ):
            for i in range( len( output ) ):
                print( output[i] )


class System:
    def execute( command: str ):
        # print( command )
        os.system( command )
    def clear():
        os.system( "cls" )
    def clear_cache():
        os.system( "rmdir /S /Q __pycache__" )
    class file:
        def write( file_name: str, content, mode: str ):
            if Type.get_type( content ) != "list":
                content = [ str( content ) ]
            file = open( file_name, mode )

            for i in range( len( content ) ):
                if content[i][len( content[i] )-1] == '\n':
                    file.write( content[i] )
                else:
                    file.write( content[i] + '\n' )

            file.close()
        def read( file_name: str ):
            return_file = []
            try:
                file = open( file_name, "r" )
                brut_file = file.read()+'\n'
                file.close()
                traitement = ""
                for i in range( len( brut_file ) ):
                    for j in range( len( brut_file[i] ) ):
                        if brut_file[i][j] == '\n':
                            return_file.append( traitement )
                            traitement = ""
                        else:
                            traitement += brut_file[i][j]
                return return_file
            except FileNotFoundError:
                return FileNotFoundError


def parrot( rgb: bool ):
    if rgb:
        System.execute( "curl parrot.live" )
    else:
        System.execute( "curl ASCII.live/parrot" )


def can_you_hear_me():
    subprocess.run( [ "curl", "ASCII.live/rick" ] )



class Json:
    def write( informations: dict, json_name: str ):
        json_object = json.dumps( informations, indent=4 )
        with open( json_name, Type.file.trunc, encoding="utf-8" ) as outfile:
            outfile.write( json_object )
    def read( json_name: str ):
        with open( json_name, Type.file.read, encoding="utf-8" ) as infile:
            informations = json.load( infile )
        return informations
    


class GoogleHome:
    class devices:
        chromecasts = 0
        browser = 0
    
    def __init__( self ):
        self.devices.chromecasts, self.devices.browser = pychromecast.get_chromecasts()

    def print_devices( self ):
        for i, cc in enumerate( self.devices.chromecasts ):
            print( f"{i + 1}. {cc.cast_info.friendly_name}" )

    def choose_device( self ):
        while True:
            try:
                choice = int( input() )
                if 1 <= choice <= len( self.devices.chromecasts ):
                    return self.devices.chromecasts[choice - 1]
                else:
                    return -1
            except ValueError:
                return -2

    def send_msg( self, tts_message, chosen_device ):
        chosen_device.wait()
        chosen_device.media_controller.play_media( f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={tts_message}&tl=fr", "audio/mp3" )
        chosen_device.media_controller.block_until_active()
        self.devices.browser.stop_discovery()



class Sound:

    def listen( language: str = "fr-FR" ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise( 1 )
            except AssertionError:
                pass
            # r.adjust_for_ambient_noise( 1 )
            audio_data = r.listen( source=source, phrase_time_limit=3 )
        try:
            text = r.recognize_google( audio_data, language=language )
            text = str( text )
            return text
        except sr.UnknownValueError:
            return -1
        except sr.RequestError:
            return -2
        

    def say( say: str, word_per_minute: int = 150, language: str = 'fr' ):
        # say = "." + say
        engine = pyttsx3.init()
        voices = engine.getProperty( "voices" )
        if language == "fr":
            engine.setProperty( "voice", voices[0].id )
        elif language == "en":
            engine.setProperty( "voice", voices[1].id )
        engine.setProperty( "rate", word_per_minute )
        engine.say( say )
        engine.runAndWait()

class Shell:
    def __init__( self, title="SHell", width=1270, height=700, backgnd_color=BLACK, txt_color=WHITE ):
        pygame.init()
        self.title = title
        self.width = width
        self.height = height
        self.screen = None
        self.running = False
        self.messages = []
        self.font = pygame.font.Font( None, 24 )
        self.background_color = backgnd_color
        self.text_color = txt_color
        self.input_text = ""
        self.lock = threading.Lock()

    def user_input( self ):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        with self.lock:
                            text = self.input_text
                            self.input_text = ""
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        with self.lock:
                            self.input_text = self.input_text[:-1]
                    else:
                        with self.lock:
                            self.input_text += event.unicode

    def show( self ):
        if self.running:
            return
        self.running = True
        self.screen = pygame.display.set_mode( ( self.width, self.height ) )
        pygame.display.set_caption( self.title )
        self.window_thread = threading.Thread( target=self._main_loop )
        self.window_thread.daemon = True
        self.window_thread.start()

    def add_message( self, message ):
        with self.lock:
            self.messages.append( message )
            if len( self.messages ) > ( self.height // 24 ):
                self.messages.pop( 0 )

    def close_window( self ):
        self.running = False
        if self.window_thread.is_alive():
            self.window_thread.join()
        pygame.quit()

    def _main_loop( self ):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill( self.background_color )

            y_offset = 10
            with self.lock:
                for message in self.messages:
                    text_surface = self.font.render( message, True, self.text_color )
                    self.screen.blit( text_surface, ( 10, y_offset ) )
                    y_offset += 24

                input_surface = self.font.render( self.input_text, True, self.text_color )
                self.screen.blit( input_surface, ( 10, y_offset ) )

            pygame.display.flip()
            clock.tick( 30 )


class AiModel:

    api_key = "e1156b809dda4345ba41a96cc4dbc00f.vX3py4XQMmdAyPLqNyBmHjkN"

    def launch():
        os.system( "ollama serve" )

    def get_all_models():
        models = ollama.list()
        if models and "models" in models:
            return [model_info["model"] for model_info in models["models"]]
        else:
            raise AiModel.OllamaError( "No Ollama models found locally." )
    
    def get_closest_model( model_name: str ):
        models = AiModel.get_all_models()
        for model in models:
            if model.lower().find( model_name.lower() ) != -1:
                return model
        raise AiModel.OllamaError( f"No Ollama model found matching '{model_name}'." )

    
    def ask( prompt, model: str = get_all_models()[0], thinking: bool = False, web: bool = False ):
        conversation = []
        if Type.getType( prompt ) == "list":
            conversation = prompt
        elif Type.getType( prompt ) == "json":
            conversation = [prompt]
        elif Type.getType( prompt ) == "str":
            conversation = [{"role": "user", "content": prompt}]
        else:
            conversation = [prompt.getPrompt()]
        
        try:
            if web:
                available_tools = {'web_search': web_search, 'web_fetch': web_fetch}
                while True:
                    response = None
                    try:
                        response = ollama.chat(
                            model=model,
                            messages=conversation,
                            think=thinking,
                            tools=[ollama.web_search, ollama.web_fetch]
                        )
                        # conversation.append( response["message"] )
                    except ollama.ResponseError as e:
                        if str( e ).find( "think" ) != -1:
                            response = ollama.chat(
                                model=model,
                                messages=conversation,
                                think=False,
                                tools=[ollama.web_search, ollama.web_fetch]
                            )
                        else:
                            raise ollama.ResponseError( "tools" )
                        

                    conversation.append( response["message"] )

                    if response.message.tool_calls:
                        for tool_call in response.message.tool_calls:
                            function_to_call = available_tools.get(tool_call.function.name)
                            if function_to_call:
                                args = tool_call.function.arguments
                                result = function_to_call(**args)
                                conversation.append({'role': 'tool', 'content': str(result), 'tool_name': tool_call.function.name})
                            else:
                                conversation.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
                    else:
                        break
                return conversation[-1]["content"].split( "</think>" )[-1], thinking, web
            else:
                response = ollama.chat( model=model, messages=conversation, think=thinking )
                return response['message']['content'].split( "</think>" )[-1], thinking, web
        except ollama.ResponseError as e:
            if str( e ).find( "tools" ) != -1:
                try:
                    return ollama.chat( model=model, messages=conversation, think=thinking )['message']['content'].split( "</think>" )[-1], thinking, False
                except ollama.ResponseError as e:
                    if str( e ).find( "think" ) != -1:
                        return ollama.chat( model=model, messages=conversation, think=False )['message']['content'].split( "</think>" )[-1], False, False
    class ChatBot:
        conversation = []
        model = ""
        thinking = False
        def __init__( self, model: str, thinkning: bool = False ):
            self.model = model
            self.thinking = thinkning
        
        def ask( self, prompt ):
            self.conversation.append( prompt.get_prompt() )
            response = ollama.chat( model=self.model, messages=self.conversation, think=self.thinking )
            model_reply = response['message']['content']
            self.conversation.append( response["message"] )
            return model_reply

    class Prompt:
        message = ""
        images = []
        cache = True
        def __init__( self, message: str, cache: bool = True, images: list = [] ):
            self.message = message
            self.cache = cache
            if cache:
                os.makedirs( "./__pycache__/aicache", exist_ok=True )
                if images != []:
                    for image in images:
                        timestamp = str( time.time() ).replace( '.', '' )
                        Image.open( image ).copy().save( "./__pycache__/aicache/" + timestamp + ".png" if image.lower().endswith( '.png' ) else "./__pycache__/aicache/" + timestamp + ".jpg" )
                        self.images.append( "./__pycache__/aicache/" + timestamp + ".png" if image.lower().endswith( '.png' ) else "./__pycache__/aicache/" + timestamp + ".jpg" )

        def loadImage( self, image_path: str ):
            image_path = image_path.replace( '\\', '/' ).replace( '"', '' )
            if not self.cache:
                self.images.append( image_path )
            else:
                timestamp = str( time.time() ).replace( '.', '' )
                img = Image.open( image_path ).copy()
                img.save( "./__pycache__/aicache/" + timestamp + ".png" if image_path.lower().endswith( '.png' ) else "./__pycache__/aicache/" + timestamp + ".jpg" )
                self.images.append( "./__pycache__/aicache/" + timestamp + ".png" if image_path.lower().endswith( '.png' ) else "./__pycache__/aicache/" + timestamp + ".jpg" )
        
        def getPrompt( self ):
            return { 'role': 'user', 'content': self.message, 'images': self.images }
        
    class OllamaError( Exception ):
        pass

System.clear()