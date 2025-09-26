import os
import subprocess
import json
from dotenv import load_dotenv
import google.genai as genai

# Load .env file
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.environ["api_key"])

# Function to run shell/command prompt commands
def run_command(command: str):
    try:
        result = subprocess.getoutput(command)
        return result
    except Exception as e:
        return f"Error executing command: {e}"

# Available tools for the model
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Execute a shell command and return its output."
    }
}

# Function to let model decide which tool to call
def call_tool(action):
    function_name = action.get("function")
    tool = available_tools.get(function_name)

    if not tool:
        return {"error": f"Tool {function_name} not found."}

    fn = tool["fn"]
    tool_input = action.get("input", "")
    return fn(tool_input)

# Main interactive loop
while True:
    user_input = input("> ")

    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        # Ask Gemini to decide next step
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
You are a helpful AI agent. The user says: "{user_input}"

Decide the next step in JSON format with one of these:
- If you need to execute a command: {{"step": "action", "function": "run_command", "input": "your_command"}}
- If you want to reply to the user directly: {{"step": "output", "message": "your message"}}
"""
        )

        # Extract text safely
        response_text = response.text.strip()
        print("think..:", response_text)

        # Try parsing JSON
        action = None
        try:
            action = json.loads(response_text)
        except json.JSONDecodeError:
            print("observe..: Could not parse model response as JSON.")
            continue

        if action["step"] == "action":
            result = call_tool(action)
            print("observe..:", result)
        elif action["step"] == "output":
            print("observe..:", action["message"])
        else:
            print("observe..: Unknown step type.")

    except Exception as e:
        print("Error:", e)
