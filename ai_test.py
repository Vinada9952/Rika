from groq import Groq


client = Groq( api_key="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" )


print(
    client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Quels sont les dernières actualités ?"
            }
        ]
    ).choices[0].message.content
)