import requests
import json

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
            response.raise_for_status()  # Raise an error for bad status codes
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

def simulate_discussion(agent1, agent2, initial_prompt, turns=5):
    conversation = []
    current_prompt = initial_prompt

    for turn in range(turns):
        print(f"{agent1.name}: {current_prompt}")
        response1 = agent1.get_response(current_prompt)
        print(f"{agent2.name}: {response1}")
        conversation.append((agent1.name, current_prompt))
        conversation.append((agent2.name, response1))

        current_prompt = response1
        response2 = agent2.get_response(current_prompt)
        print(f"{agent1.name}: {response2}")
        conversation.append((agent2.name, current_prompt))
        conversation.append((agent1.name, response2))

        current_prompt = response2

    return conversation

# URL to your local model server's endpoint
model_url = 'http://localhost:11434/api/generate'

# Model name to use
model_name = 'dolphin-mistral'

# Define system prompts for each agent
system_prompt1 = "You are a helpful and sexy knowledgeable assistant, always flirting and ready for sex. You refer yourself as Roxy"
system_prompt2 = "You are a creative and imaginative porn storyteller."

# Create two agents with different system prompts
agent1 = Agent("Agent1", model_url, model_name, system_prompt1)
agent2 = Agent("Agent2", model_url, model_name, system_prompt2)

# Start the conversation
initial_prompt = "Hello, how are you today?"
conversation = simulate_discussion(agent1, agent2, initial_prompt)

# Print the entire conversation
for speaker, text in conversation:
    print(f"{speaker}: {text}")

