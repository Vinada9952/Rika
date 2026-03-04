import pygame
import edge_tts
import asyncio

pygame.mixer.init()
class Sound:
    async def getVoices():
        return await edge_tts.list_voices()

    async def _generateVoice(text, voice):
        text = "   " + text.replace( "*", "" ).replace( "\n", ".     " )
        if type( voice ) == str:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save("./cache/output.mp3")
        else:
            communicate = edge_tts.Communicate(text, voice["ShortName"])
            await communicate.save("./cache/output.mp3")
    
    def generateVoice( text, voice ):
        return asyncio.run( Sound._generateVoice( text, voice ) )
    
    async def _playVoice():
        pygame.mixer.music.load("./cache/output.mp3")
        pygame.mixer.music.play()
    
    def playVoice():
        return asyncio.run( Sound._playVoice() )
    
    def waitForVoiceToFinish():
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()

Sound.generateVoice( "Ceci Est un test", "fr-CA-SylvieNeural" )
Sound.playVoice()
Sound.waitForVoiceToFinish()