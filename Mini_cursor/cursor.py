import json
import requests
from openai import OpenAI


from dotenv import load_dotenv
from groq import Groq
import os
import subprocess

load_dotenv()

client = OpenAI()

def create_file(params: dict):
    
    try:
        path = params.get("path")
        content = params.get("content", "")

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ File created at {path}"
    except Exception as e:
        return f"❌ Error creating file: {e}"


# def run_command(command: str):
#     try:
#         result = subprocess.getoutput(command)
#         return result
#     except Exception as e:
#         return f"Error executing command: {e}"

def run_command(command):
    result = os.system(command)  
    return result

def get_weather(city: str):
    # TODO!: Do an actual API call
    print(" Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong!"



available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    }, 
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a file at the given path with the provided content"
    }
}

system_prompt = f"""
    You are a mini Cursor AI, an helpful AI Assistant who is specialized in resolving user query in programming. A coding copilot inside a text editor.
    You work on start, plan, observe mode. 
    For the given user query and available tools, plan the step by step execution, based on the planning, select the relevant tool from the available tools.
    And based on the tool selection you perform an action to call the tool. 
    Wait for the observation and based on the observation from the tool call resolve the user query. 

    
    Rules: 
    - Always wait for next step.
    - Never output multiple JSON objects at once.
    - Always output a single step and wait for the next step.
    - Output must be strictly JSON
    - Only call tool action from Available tools
    - Follow strictly the output in JSON Formate. 
    - Always perform one step at a time and wait for the next input
    - Carefully analyse the user query


    output JSON Formate:
    {{
        "step": "string", 
        "content": "string", 
        "function": "The name of the function if the step is action",
        "input": "The input parameter for the function"        
    }}

    Available Toools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns output
    - create_file: Creates a file at the given path with the provided content

    Example: 
    User Query: What is the wather of new york?
    Output: {{"step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{"step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{"step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{"step": "observe", "output": "12 Degree Cel"}}
    Output: {{"step": "output", "content": "The weather of new york seems to be 12 Degree Cel"}}

"""


messages = [
    {"role": "system", "content": system_prompt},    
]

while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model = "gpt-4.1",
            response_format={'type': "json_object"},
            messages = messages

        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"think..: {parsed_output.get('content')}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue
        
        if parsed_output.get("step") == "output":
            print(f"final output..: {parsed_output.get('content')}")
            break

            


