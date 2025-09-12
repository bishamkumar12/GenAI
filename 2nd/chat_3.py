import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()


system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and resolve the user query.

For the given user input, analyse the input and beak down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down. 

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules: 
1. Follow the strict JSON output as per Output schema. 
2. Always perform one step at a time and wait for the next input
3. Carefully analyse the user query

Output Formate:
{{Step: "string", content: "string"}}

Example: 
Input: what is 2 + 2.
Output: {{Step: "analyse", content: "Alright! The user is intersted in maths quey and he is asking a basic arthmetic operation"}}
Output: {{step: "think", content: "To perform the addition I must go from left to right and add all the operands"}}
Output: {{step: "output", content: "4"}}
Output: {{step: "validate", content: "seems like 4 is correct ans for 2 + 2"}}
Output: {{step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}
"""


result = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    response_format={'type': 'json_object'},
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": "what is 3 + 4 * 5"}, 

        #
        {"role": "assistant", "content": json.dumps({"Step":"analyse","content":"User asks to compute arithmetic expression 3 + 4 * 5, which involves operator precedence (multiplication before addition)."})},
        {"role": "assistant", "content": json.dumps({"Step":"think","content":"Apply order of operations: first compute 4 * 5 = 20, then add 3 + 20 = 23."})}
               

    ]
)

print(result.choices[0].message.content)