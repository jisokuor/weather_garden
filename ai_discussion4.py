import requests
import json
import sys

# Ensure UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

class Agent:
    def __init__(self, name, model_url, model_name, system_prompt):
        self.name = name
        self.model_url = model_url
        self.model_name = model_name
        self.system_prompt = system_prompt

    def get_response(self, prompt):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'model': self.model_name,
            'prompt': f"{self.system_prompt}\n{prompt}",
            'stream': False
        }
        try:
            response = requests.post(self.model_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_json = response.json()
            return response_json['response']
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Error: Request failed"

def simulate_discussion(agents, initial_prompt, turns=5):
    conversation = []
    current_prompt = initial_prompt

    for turn in range(turns):
        for agent in agents:
            print(f"{agent.name}: {current_prompt}")
            response = agent.get_response(current_prompt)
            print(f"{agent.name}: {response}")
            conversation.append((agent.name, current_prompt))
            current_prompt = response

    return conversation

# URL to your local model server's endpoint
model_url = 'http://localhost:11434/api/generate'

# Model name to use
model_name = 'dolphin-mistral'

# Get user instructions for each family member
system_prompt_mother = input("Describe how the mother should act: ")
system_prompt_father = input("Describe how the father should act: ")
system_prompt_daughter = input("Describe how the daughter should act: ")

# Create three agents representing family members
mother = Agent("Mother", model_url, model_name, system_prompt_mother)
father = Agent("Father", model_url, model_name, system_prompt_father)
daughter = Agent("Daughter", model_url, model_name, system_prompt_daughter)

# Aggregate agents into a list
agents = [mother, father, daughter]

# Start the conversation
initial_prompt = "Good morning everyone! What are our plans for today?"
conversation = simulate_discussion(agents, initial_prompt)

# Print the entire conversation
for speaker, text in conversation:
    print(f"{speaker}: {text}")
