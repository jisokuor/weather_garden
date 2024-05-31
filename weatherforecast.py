import config
import requests
import json
from gtts import gTTS
import subprocess
import os
from datetime import datetime
from bs4 import BeautifulSoup

# System prompts for weather and gardening
system_prompt_weather = """
As a certified weather forecast expert using the metric system, I am equipped to provide comprehensive assistance in reading and interpreting weather data using official meteorological standards.
Avoid using '*' in your output"""

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
        f"- Temperature: {temperature}\n"
        f"- Weather conditions: {weather_description}\n"
        f"- Wind speed: {wind_speed} m/s\n"
        f"- Humidity: {humidity}%\n\n"
        f"Month: {datetime.now().strftime('%B')}\n"
        f"Weather data (in JSON): {json.dumps(weather_data, indent=2)}")

    return query_ollama(prompt, system_prompt_gardening, config.MODEL_URL)


def text_to_speech(text, filename='forecast.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)


def update_index_html(mp3_files, daily_forecast, dynamic_gardening_tips):
    html_file_path = "index.html"
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast and Gardening Tips</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        header {{
            text-align: center;
            padding: 20px;
            background-color: #2E8B57;
            color: white;
            margin-bottom: 20px;
        }}
        h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        h2 {{
            color: #2E8B57;
            font-size: 1.8em;
        }}
        h3 {{
            color: #555;
            font-size: 1.4em;
            margin-top: 20px;
        }}
        p {{
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .mp3-links {{
            margin-top: 20px;
        }}
        .clock {{
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Daily Weather Forecast and Gardening Tips</h1>
        <h2>Date: <span id="date">{datetime.now().strftime("%B %d, %Y")}</span></h2>
    </header>
    <div class="container">
        <div class="clock">
            <h3>Current Time</h3>
            <iframe src="https://indify.co/widgets/live/clock/mC6PDMEhkRcvdRHnRtuG" style="border:none;width:100%;height:100px;"></iframe>
        </div>
        <section>
            <h3>Weather Forecast</h3>
            <p id="weather-forecast">{daily_forecast.replace('<p></p>', '<br>')}</p>
        </section>
        <section>
            <h3>Dynamic Gardening Tips</h3>
            <p id="dynamic-gardening-tips">{dynamic_gardening_tips.replace('<p></p>', '<br>')}</p>
        </section>
        <section class="mp3-links">
            <h3>Download MP3 Files</h3>
            <ul id="mp3-links">""")

        for mp3_file in mp3_files:
            file.write(f'<li><a href="{mp3_file}" download>{mp3_file}</a></li>\n')

        file.write("""            </ul>
        </section>
    </div>
</body>
</html>""")


def save_markdown(daily_forecast, dynamic_gardening_tips):
    with open('output.md', 'w', encoding='utf-8', errors='replace') as file:
        file.write("# Weather Forecast and Gardening Tips\n")
        file.write(f"## Date: {datetime.now().strftime('%B %d, %Y')}\n")
        file.write("\n## Weather Forecast\n")
        file.write(daily_forecast)
        file.write("\n## Dynamic Gardening Tips\n")
        file.write(dynamic_gardening_tips)


def commit_and_push_changes():
    subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"])
    subprocess.run(["git", "add", "-f", "index.html", "forecast.mp3", "gardening_tips.mp3", "output.md",
                    "weatherforecast.py", "requirements.txt", "run_daily_update.bat"])
    subprocess.run(["git", "commit", "-m", "Daily weather and gardening tips update"])
    subprocess.run(["git", "push", "origin", "main"])


def extract_weather_data_from_html(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    weather_forecast_section = soup.find(id='weather-forecast')
    if weather_forecast_section is None:
        raise Exception("Weather forecast section not found in HTML.")

    weather_forecast_text = weather_forecast_section.text.strip()
    print(f"Extracted weather text: {weather_forecast_text}")

    weather_data = {}
    for line in weather_forecast_text.split('\n'):
        print(f"Processing line: {line}")
        if 'Current Temperature' in line:
            weather_data['temperature'] = line.split(':')[1].strip()
        elif 'Feels like' in line:
            weather_data['feels_like'] = line.split(':')[1].strip()
        elif 'Weather Conditions' in line:
            weather_data['weather_description'] = line.split(':')[1].strip()
        elif 'Wind Speed' in line:
            weather_data['wind_speed'] = line.split(':')[1].strip().split()[0]
        elif 'Humidity' in line:
            weather_data['humidity'] = line.split(':')[1].strip().replace('%', '')
        elif 'Pressure' in line:
            weather_data['pressure'] = line.split(':')[1].strip().split()[0]

    print(f"Extracted weather data: {weather_data}")
    return weather_data


def main():
    html_file_path = 'index.html'

    try:
        weather_data = extract_weather_data_from_html(html_file_path)
        dynamic_gardening_tips = gardening_tips(weather_data)
        print(f"Generated gardening tips: {dynamic_gardening_tips}")

        text_to_speech(dynamic_gardening_tips, filename='gardening_tips.mp3')

        update_index_html(['gardening_tips.mp3'], '', dynamic_gardening_tips)
        save_markdown('', dynamic_gardening_tips)
        commit_and_push_changes()

    except Exception as e:
        print(f"Failed to retrieve or translate weather data: {str(e)}")


if __name__ == "__main__":
    main()

