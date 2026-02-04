from Vincent import *

# AiModel.launch()
print( AiModel.get_all_models() )

prompt = AiModel.Prompt( "Dit moi dans quel bac ce déchet va, poubelle, composte ou recyclage" )
prompt.loadImage( "C:/Users/Vinad/Downloads/326190.jpg" )
response = AiModel.ask( prompt, AiModel.get_closest_model( "gemma" ), False, False )
print( response[0] )