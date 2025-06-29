from google import genai
from google.genai import types


client = genai.Client( api_key="AIzaSyDR-OOUGNxmInqrIC5qQEAfUnqX4XR3qRY" )

myfile = client.files.upload(file="./request.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[myfile]
)

print(response.text)