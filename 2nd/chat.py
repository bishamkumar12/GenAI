from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

result = client.chat.completions.create(
    model = "openai/gpt-oss-120b", 
    messages = [
        {'role': 'user', 'content': "hey there"} # Zero shot prompting
        ]
)


print(result)

print('\n', result.choices[0].message.content)