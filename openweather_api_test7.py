import requests
import json
from gtts import gTTS
import pygame
from datetime import datetime  # Import the datetime module

# Display the system prompt for the user
system_prompt_weather = """
As a certified weather forecast expert using the metric system, I am equipped to provide comprehensive assistance in reading and interpreting weather data using official meteorological standards. For more information, please upload relevant documents to Open WebUI: <https://docs.openwebui.com>.
"""

system_prompt_gardening = """
As the Gardener of the Year of Porvoo, I offer expert gardening tips and recommendations based on the current weather forecast. For more information, please upload relevant documents to Open WebUI: <https://docs.openwebui.com>.
"""


def query_ollama(prompt, system_message, model_url='http://localhost:11434/api/generate'):
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


def test_openweathermap_api(api_key):
    lat = "60.4720597"
    lon = "25.7878047"
    exclude = "minutely,daily"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        print("API key is working!")
        return response.json()
    elif response.status_code == 401:
        raise Exception("Invalid API key.")
    else:
        raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def get_next_3_hours_data(weather_data):
    return {
        "list": weather_data["list"][:3],
        "city": weather_data["city"]
    }


def translate_weather_data(weather_data):
    weather_data_json = json.dumps(weather_data, indent=2)
    prompt = (
        f"The weather data provided is in 3-hour intervals. Read the weather forecast based on this data. The data is in metric units. Start with: **Current Weather:** "
        f"Include specific details about the current temperature in Celsius, weather conditions, wind speed in meters per second, visibility, "
        f"and any other relevant details in a clear and concise manner as you would hear it on a weather report. "
        f"Format it as follows:\n"
        f"1. **Date and Time**\n"
        f"2. **Temperature**: Current, Feels like, Min, Max\n"
        f"3. **Weather Conditions**: Description\n"
        f"4. **Wind**: Speed, Direction, Gust\n"
        f"5. **Visibility**\n"
        f"6. **Humidity**\n"
        f"7. **Pressure**\n\n"
        f"The data is found inside this: {weather_data_json}. Translate it to the actual weather forecast. "
        f"The data is derived today from openweather.com and is up to date.")
    return query_ollama(prompt, system_prompt_weather)


def gardening_tips(weather_data):
    weather_data_json = json.dumps(weather_data, indent=2)
    prompt = (
        f"Based on the following weather data, which is in 3-hour intervals, provide expert gardening tips and recommendations for today. "
        f"Offer advice on watering, setting shades, what to plant today, and other useful hints and tips. Common sense used, check the month as we live in Finland Porvoo\n\n"
        f"Weather data: {weather_data_json}")
    return query_ollama(prompt, system_prompt_gardening)


def text_to_speech(text, filename='forecast.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def commit_and_push_changes():
    import subprocess
    subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"])
    subprocess.run(["git", "add", "-f", "index.html", "forecast.mp3", "gardening_tips.mp3", "output.md"])
    subprocess.run(["git", "commit", "-m", "Daily weather and gardening tips update"])
    subprocess.run(["git", "push", "origin", "main"])


def main():
    api_key = "918403ad1a1997bf8650f34d05c9c9a4"
    print(system_prompt_weather)
    try:
        weather_data = test_openweathermap_api(api_key)
        next_3_hours_data = get_next_3_hours_data(weather_data)

        daily_forecast = translate_weather_data(next_3_hours_data)
        print("\nDaily Weather Forecast:")
        print(daily_forecast)

        gardening_advice = gardening_tips(daily_forecast)
        print("\nGardening Tips:")
        print(gardening_advice)

        # Generate audio files for the forecast and gardening tips
        text_to_speech(daily_forecast, filename='forecast.mp3')
        text_to_speech(gardening_advice, filename='gardening_tips.mp3')

        # Save the results to a Markdown file
        with open('output.md', 'w') as file:
            file.write("# Daily Weather Forecast and Gardening Tips\n")
            file.write("## Date: " + datetime.now().strftime("%B %d, %Y") + "\n")
            file.write("\n## Weather Forecast\n")
            file.write(daily_forecast)
            file.write("\n## Gardening Tips\n")
            file.write(gardening_advice)

        # Save the results to an HTML file
        with open('index.html', 'w') as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html lang='en'>\n")
            file.write("<head>\n")
            file.write("    <meta charset='UTF-8'>\n")
            file.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
            file.write("    <title>Daily Weather Forecast and Gardening Tips</title>\n")
            file.write("    <style> body { font-family: Arial, sans-serif; margin: 20px; } h1 { color: #2E8B57; } </style>\n")
            file.write("</head>\n")
            file.write("<body>\n")
            file.write("<h1>Daily Weather Forecast and Gardening Tips</h1>\n")
            file.write("<h2>Date: " + datetime.now().strftime("%B %d, %Y") + "</h2>\n")
            file.write("<h3>Weather Forecast</h3>\n")
            file.write("<p>" + daily_forecast.replace('\n', '<br>') + "</p>\n")
            file.write("<h3>Gardening Tips</h3>\n")
            file.write("<p>" + gardening_advice.replace('\n', '<br>') + "</p>\n")
            file.write("</body>\n")
            file.write("</html>")

        # Commit and push changes
        commit_and_push_changes()

    except Exception as e:
        print(f"Failed to retrieve or translate weather data: {str(e)}")


if __name__ == "__main__":
    main()