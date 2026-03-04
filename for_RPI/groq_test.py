from groq import Groq
from groq import RateLimitError
from groq import APIStatusError
import time

groq_client = Groq( api_key="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" )

def askGroq( model, prompt ):
    global groq_client

    retries = 0
    while True:
        if retries != 10 + 1:
            try:
                response = groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                ).choices[0].message.content
                break
            except APIStatusError:
                time.sleep( 0.5 )
                retries += 1
                # print(  )
            except RateLimitError:
                time.sleep( 0.5 )
                # retries += 1
        else:
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            ).choices[0].message.content
            break
    
    return response

print( askGroq( "llama-3.1-8b-instant", "Qui es-tu ?" ) )