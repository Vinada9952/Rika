from ollama import chat, web_fetch, web_search
from Vincent import *

available_tools = {'web_search': web_search, 'web_fetch': web_fetch}

messages = [{'role': 'user', 'content': "va chercher sur internet les dernières nouvelles sur l'ia"}]

while True:
    response = chat(
            model=AiModel.get_closest_model( "qwen" ),
            messages=messages,
            tools=[web_search, web_fetch],
            think=True
        )
    
    if response.message.thinking:
        print('\n\n-----------------Thinking: ', response.message.thinking)
    if response.message.content:
        print('\n\n-----------------Content: ', response.message.content)
    messages.append(response.message)
    if response.message.tool_calls:
        print('\n\n-----------------Tool calls: ', response.message.tool_calls)
        for tool_call in response.message.tool_calls:
            function_to_call = available_tools.get(tool_call.function.name)
            if function_to_call:
                args = tool_call.function.arguments
                result = function_to_call(**args)
                print('\n\n-----------------Result: ', str(result)[:200]+'...')
                # Result is truncated for limited context lengths
                messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})
            else:
                messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
    else:
        break