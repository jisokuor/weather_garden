import config
import requests
import json
from gtts import gTTS
from datetime import datetime
import subprocess
from bs4 import BeautifulSoup

# System prompts for weather and gardening
system_prompt_gardening = """
As the Gardener of the Year of Porvoo, I offer expert gardening tips and recommendations based on the current weather forecast.
Avoid using '*' in your output"""


def query_ollama(prompt, system_message, model_url):
    data = {
        'model': 'llama3',
        'prompt': prompt,
        'system': system_message
    }
    response = requests.post(model_url, json=data, stream=True)
    if response.status_code == 200:
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line.decode('utf-8'))
                    full_response += decoded_line['response']
                    if decoded_line.get('done', False):
                        break
            return full_response.strip()
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}")
    else:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")


def extract_weather_data_from_html(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        weather_forecast_section = soup.find('section', {'id': 'weather-forecast-section'})
        if weather_forecast_section is None:
            raise Exception("Weather forecast section not found in HTML.")

        weather_text = weather_forecast_section.find('p', {'id': 'weather-forecast'}).text.strip()
        print(f"Extracted weather text: {weather_text}")  # Debug print
        weather_lines = weather_text.split('\n')

        weather_data = {}
        for line in weather_lines:
            line = line.strip()  # Remove leading and trailing whitespace
            print(f"Processing line: {line}")  # Debug print
            if "Temperature:" in line:
                weather_data['temperature'] = line.split(":")[1].strip().split(' ')[0]
            elif "Feels like:" in line:
                weather_data['feels_like'] = line.split(":")[1].strip().split(' ')[0]
            elif "Weather:" in line:
                weather_data['weather_description'] = line.split(":")[1].strip()
            elif "Wind speed:" in line:
                weather_data['wind_speed'] = line.split(":")[1].strip().split(' ')[0]
            elif "Humidity:" in line:
                weather_data['humidity'] = line.split(":")[1].strip().split(' ')[0].replace('%', '')
            elif "Pressure:" in line:
                weather_data['pressure'] = line.split(":")[1].strip().split(' ')[0]

        print(f"Extracted weather data: {weather_data}")  # Debug print
        return weather_data


def gardening_tips(weather_data):
    temperature = weather_data['temperature']
    weather_description = weather_data['weather_description']
    wind_speed = weather_data['wind_speed']
    humidity = weather_data['humidity']

    prompt = (
        f"Based on the following weather data, which is in 3-hour intervals, provide expert gardening tips and recommendations for today in Porvoo, Finland. "
        f"Offer advice on watering, setting shades, what to plant today, and other useful hints and tips. "
        f"Use common sense and take into account the month as well as the weather conditions.\n\n"
        f"Weather data:\n"
        f"- Temperature: {temperature}°C\n"
        f"- Weather conditions: {weather_description}\n"
        f"- Wind speed: {wind_speed} m/s\n"
        f"- Humidity: {humidity}%\n\n"
        f"Month: {datetime.now().strftime('%B')}\n"
    )

    return query_ollama(prompt, system_prompt_gardening, config.MODEL_URL)


def text_to_speech(text, filename='forecast.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)


def update_index_html(mp3_files, gardening_tips_text):
    html_file_path = "weatherforecast.html"
    with open(html_file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')

    gardening_tips_section = soup.find('section', {'id': 'gardening-tips-section'})
    if gardening_tips_section:
        gardening_tips_paragraph = gardening_tips_section.find('p', {'id': 'gardening-tips'})
        gardening_tips_paragraph.string = gardening_tips_text

    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def save_markdown(gardening_tips_text):
    with open('output.md', 'w', encoding='utf-8', errors='replace') as file:
        file.write("# Gardening Tips\n")
        file.write(f"## Date: {datetime.now().strftime('%B %d, %Y')}\n")
        file.write("\n## Gardening Tips\n")
        file.write(gardening_tips_text)


def commit_and_push_changes():
    subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"])
    subprocess.run(["git", "add", "-f", "weatherforecast.html", "output.md", "weatherforecast.py"])
    subprocess.run(["git", "commit", "-m", "Daily gardening tips update"])
    subprocess.run(["git", "push", "origin", "main"])


def main():
    html_file_path = 'weatherforecast.html'
    try:
        weather_data = extract_weather_data_from_html(html_file_path)
        gardening_tips_text = gardening_tips(weather_data)
        print(f"Generated gardening tips: {gardening_tips_text}")  # Debug print

        text_to_speech(gardening_tips_text, filename='gardening_tips.mp3')

        update_index_html(['gardening_tips.mp3'], gardening_tips_text)
        save_markdown(gardening_tips_text)
        commit_and_push_changes()

    except Exception as e:
        print(f"Failed to retrieve or translate weather data: {str(e)}")


if __name__ == "__main__":
    main()
