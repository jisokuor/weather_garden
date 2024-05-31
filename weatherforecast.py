import os
import config
import requests
import json
from gtts import gTTS
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import config  # Import the config module

app = Flask(__name__)

API_KEY = config.OPEN_WEATHER_API_KEY  # Use the API key from the config module
LAT = '60.4720597'
LON = '25.7878047'

@app.route('/fetch_weather_data')
def fetch_weather_data():
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('weatherforecast.html')

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


def extract_weather_data_from_html(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    weather_forecast_section = soup.find(id='weather-forecast')
    if not weather_forecast_section:
        raise Exception("Weather forecast section not found in HTML.")

    weather_text = weather_forecast_section.get_text(separator="\n").strip()
    print("Extracted weather text:", weather_text)

    weather_data = {}
    for line in weather_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            weather_data[key.strip().lower().replace(' ', '_')] = value.strip()

    print("Parsed weather data:", weather_data)
    return weather_data


def gardening_tips(weather_data):
    temperature = weather_data['temperature']
    weather_description = weather_data['weather']
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
        f"Weather data (in JSON): {json.dumps(weather_data, indent=2)}")

    return query_ollama(prompt, system_prompt_gardening, config.MODEL_URL)


def text_to_speech(text, filename='forecast.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)


def save_gardening_tips_to_file(tips, filename='dynamic_gardening_tips.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tips)
    print(f"Gardening tips saved to {filename}")


def update_weatherforecast_html(weather_data, gardening_tips, labels, temps, feels_like_temps):
    with open('weatherforecast.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    date_span = soup.find(id='date')
    if date_span:
        date_span.string = datetime.now().strftime('%B %d, %Y')

    timestamp_p = soup.find(id='timestamp')
    if timestamp_p:
        timestamp_p.string = datetime.now().strftime('%H:%M:%S')

    weather_forecast_p = soup.find(id='weather-forecast')
    if weather_forecast_p:
        weather_forecast_p.string = f"""
        Temperature: {weather_data['temperature']} °C
        Feels like: {weather_data['feels_like']} °C
        Weather: {weather_data['weather']}
        Wind speed: {weather_data['wind_speed']} m/s
        Humidity: {weather_data['humidity']} %
        Pressure: {weather_data['pressure']} hPa
        """

    gardening_tips_p = soup.find(id='gardening-tips')
    if gardening_tips_p:
        gardening_tips_p.string = gardening_tips

    with open('weatherforecast.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    plot_weather_chart(labels, temps, feels_like_temps)


def plot_weather_chart(labels, temps, feels_like_temps):
    # Ensure the 'static' directory exists
    os.makedirs('static', exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(labels, temps, label='Temperature (°C)', color='b')
    plt.plot(labels, feels_like_temps, label='Feels Like (°C)', color='r')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title('Hourly Weather Forecast')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/weather_chart.png')
    plt.close()


def get_weather_forecast(api_key):
    lat = "60.4720597"
    lon = "25.7878047"
    exclude = "minutely,daily"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        print("API key is working!", response)
        return weather_data
    except requests.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def parse_weather_data(weather_data):
    forecast = weather_data['list'][:8]  # Next 8 three-hour intervals
    labels = [datetime.fromtimestamp(item['dt']).strftime('%H:%M') for item in forecast]
    temps = [item['main']['temp'] for item in forecast]
    feels_like_temps = [item['main']['feels_like'] for item in forecast]

    current_weather = forecast[0]['main']
    weather_description = forecast[0]['weather'][0]['description']

    parsed_data = {
        'temperature': current_weather['temp'],
        'feels_like': current_weather['feels_like'],
        'weather': weather_description,
        'wind_speed': forecast[0]['wind']['speed'],
        'humidity': current_weather['humidity'],
        'pressure': current_weather['pressure']
    }

    return parsed_data, labels, temps, feels_like_temps


def main():
    api_key = config.OPEN_WEATHER_MAP_API_KEY
    model_url = config.MODEL_URL

    try:
        weather_data = get_weather_forecast(api_key)
        parsed_data, labels, temps, feels_like_temps = parse_weather_data(weather_data)

        gardening_tips_text = gardening_tips(parsed_data)
        print("Generated gardening tips:", gardening_tips_text)

        # Save the dynamic gardening tips to a file
        save_gardening_tips_to_file(gardening_tips_text)

        # Update the weatherforecast.html file
        update_weatherforecast_html(parsed_data, gardening_tips_text, labels, temps, feels_like_temps)

    except Exception as e:
        print(f"Failed to retrieve or translate weather data: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
