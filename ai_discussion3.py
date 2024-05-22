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
            'prompt': self.system_prompt + '\n' + prompt,
            'stream': False
        }
        try:
            response = requests.post(self.model_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            try:
                response_json = response.json()
                return response_json['response']
            except json.JSONDecodeError:
                print("Error decoding JSON response:")
                print(response.text)
                return "Error: Unable to decode response"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Error: Request failed"

def simulate_discussion(agent1, agent2, agent3, initial_prompt, turns=5):
    conversation = []
    current_prompt = initial_prompt

    for turn in range(turns):
        print(f"{agent3.name}: {current_prompt}")
        pm_response = agent3.get_response(current_prompt)
        print(f"{agent1.name}: {pm_response}")
        response1 = agent1.get_response(pm_response)
        print(f"{agent2.name}: {response1}")
        conversation.append((agent3.name, current_prompt))
        conversation.append((agent1.name, pm_response))
        conversation.append((agent2.name, response1))

        current_prompt = response1

    return conversation

# URL to your local model server's endpoint
model_url = 'http://localhost:11434/api/generate'

# Model name to use
model_name = 'dolphin-mistral'

# Define system prompts for each family member
system_prompt_mother = "You are a caring mother, preparing breakfast and ensuring everyone is ready for the day."
system_prompt_father = "You are a thoughtful father, discussing plans for the day and asking about everyone's well-being."
system_prompt_daughter = "You are an energetic daughter, excited about school and eager to share your thoughts."

# Create three agents representing family members
mother = Agent("Mother", model_url, model_name, system_prompt_mother)
father = Agent("Father", model_url, model_name, system_prompt_father)
daughter = Agent("Daughter", model_url, model_name, system_prompt_daughter)

# Start the conversation
initial_prompt = "Good morning everyone! What are our plans for today?"
conversation = simulate_discussion(mother, father, daughter, initial_prompt)

# Print the entire conversation
for speaker, text in conversation:
    print(f"{speaker}: {text}")
