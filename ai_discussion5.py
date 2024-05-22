import os
import json
import requests
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
            'max_tokens': 3000,
            'stream': False
        }
        try:
            response = requests.post(self.model_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_json = response.json()
            return response_json['response']
        except KeyError as e:
            print("KeyError:", e)
            print("Response JSON does not have the expected format.")
            print("Response JSON content:", response_json)
            return "Error: Unexpected response format"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Error: Request failed"

def simulate_discussion(agents, initial_prompt, total_rounds=100, skip_rounds=50):
    conversation = []
    current_prompt = initial_prompt
    for round_number in range(total_rounds):
        for i, agent in enumerate(agents):
            response = agent.get_response(current_prompt)
            if round_number >= skip_rounds:
                print(f"{agent.name}: {response}")
                conversation.append((agent.name, response))
            current_prompt = response if i < len(agents) - 1 else initial_prompt  # Reset prompt for next round
            if "TERMINATE" in response:
                return conversation
    return conversation

# URL to your local model server's endpoint
model_url = 'http://localhost:11434/api/generate'

# Model name to use
model_name = 'wizard-vicuna-uncensored'

# Define system prompts for each agent
system_prompt_mother = "You are Mima, a cheerful and caring person. Speak briefly and positively."
system_prompt_father = "You are Male, a happy and optimistic individual. Speak briefly and enthusiastically."
system_prompt_daughter = "You are Cindy, a moody adult female who expresses feelings openly. Speak briefly and dramatically."

# Create agents
mother = Agent("Mima", model_url, model_name, system_prompt_mother)
father = Agent("Male", model_url, model_name, system_prompt_father)
daughter = Agent("Cindy", model_url, model_name, system_prompt_daughter)

# List of agents
agents = [mother, father, daughter]

# Start the conversation
initial_prompt = "Good morning everyone! What are our plans for today?"
conversation = simulate_discussion(agents, initial_prompt)

# Print the conversation
for speaker, text in conversation:
    print(f"{speaker}: {text}")

