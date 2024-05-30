import requests
from bs4 import BeautifulSoup
import subprocess

def fetch_available_models():
    """Fetch the list of available Ollama models from the website."""
    url = "https://ollama.com/library"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        models = []
        for model in soup.find_all('h2'):  # Modify the tag based on actual HTML structure
            models.append(model.get_text(strip=True))
        return models
    else:
        print("Failed to retrieve models.")
        return []

def check_model_installed(model_name):
    """Check if the specified Ollama model is installed."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True, timeout=30)
        installed_models = result.stdout.splitlines()
        print("Installed models:\n", result.stdout)  # Debugging output
        # Check if the exact model_name (with version) is in the installed models list
        return any(model_name in model for model in installed_models)
    except subprocess.TimeoutExpired:
        print("The command 'ollama list' timed out.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking installed models: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def install_model(model_name):
    """Install the specified Ollama model."""
    try:
        print(f"Installing Ollama model: {model_name}")
        result = subprocess.run(['ollama', 'pull', model_name], capture_output=True, text=True, check=True, timeout=300)
        if result.returncode == 0:
            print(f"Model {model_name} installed successfully.")
        else:
            print(f"Failed to install model {model_name}: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"The command 'ollama pull {model_name}' timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install model {model_name}: {e.stderr}")
    except Exception as e:
        print(f"Error during model installation: {e}")

def display_available_models(available_models):
    """Display available models."""
    print("Available Ollama models:")
    for idx, model in enumerate(available_models, 1):
        print(f"{idx}. {model}")

def main():
    available_models = fetch_available_models()
    if not available_models:
        print("No available models retrieved.")
        return

    display_available_models(available_models)

    try:
        model_index = int(input(f"Enter the number of the Ollama model you want to use (1-{len(available_models)}): "))
        if 1 <= model_index <= len(available_models):
            model_name = available_models[model_index - 1]
            print(f"Selected model: {model_name}")  # Debugging output
            if check_model_installed(model_name):
                print(f"The model '{model_name}' is already installed.")
            else:
                print(f"The model '{model_name}' is not installed.")
                install_model(model_name)
        else:
            print(f"Invalid selection. Please enter a number between 1 and {len(available_models)}.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
