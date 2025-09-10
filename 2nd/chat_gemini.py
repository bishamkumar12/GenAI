from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyDuJK_sHhHJvmyCaRZa-HqFHyXlH4oXoaI')

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents="why is the sky blue?"
)
print(response)
print()
print(response.text)