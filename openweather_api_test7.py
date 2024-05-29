# -*- coding: utf-8 -*-

import config
import requests
import json
from gtts import gTTS
import pygame
from datetime import datetime

# Display the system prompt for the user
system_prompt_weather = """
As a certified weather forecast expert using the metric system, I am equipped to provide comprehensive assistance in reading and interpreting weather data using official meteorological standards.
"""

system_prompt_gardening = """
As the Gardener of the Year of Porvoo, I offer expert gardening tips and recommendations based on the current weather forecast.
"""


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
    return query_ollama(prompt, system_prompt_weather, config.MODEL_URL)


def gardening_tips(weather_data):
    weather_data_json = json.dumps(weather_data, indent=2)
    first_forecast = weather_data["list"][0]
    temperature = first_forecast["main"]["temp"]
    weather_description = first_forecast["weather"][0]["description"]
    wind_speed = first_forecast["wind"]["speed"]
    humidity = first_forecast["main"]["humidity"]

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
        f"Weather data (in JSON): {weather_data_json}")

    return query_ollama(prompt, system_prompt_gardening, config.MODEL_URL)


def get_conditional_gardening_tips(month, weather_data):
    # Static expert advice for each month
    monthly_gardening_tips = {
        "January": "January is the coldest month in Finland, so focus on planning your garden for the upcoming year. Order seeds, clean and repair tools, and consider starting some plants indoors.",
        "February": "Continue planning and preparing. Do not plant outside, even if the weather seems warm. Start sowing seeds indoors for early vegetables like onions, leeks, and cabbage. Prune fruit trees and bushes to promote healthy growth.",
        "March": "As the weather starts to warm slightly, begin sowing seeds indoors for tomatoes, peppers, and herbs. Prepare your garden beds by adding compost and organic matter.",
        "April": "Plant cool-season crops like peas, lettuce, and spinach directly into the garden. Protect young plants from late frosts using cloches or fleece.",
        "May": "This is the main planting month. Plant potatoes, carrots, and beets. Harden off indoor-grown seedlings before transplanting them outside. Start planting summer flowers.",
        "June": "Water regularly and mulch around plants to retain moisture. Thin out seedlings and continue planting beans, corn, and summer squash. Watch for pests and take action as needed.",
        "July": "Harvest early crops like lettuce, radishes, and strawberries. Continue watering and weeding. Plant late-season crops like kale and Brussels sprouts for autumn harvest.",
        "August": "Harvest a wide variety of vegetables. Begin preparing for the fall by planting garlic and onions. Collect seeds from flowering plants to use next year.",
        "September": "Continue harvesting. Start cleaning up the garden, removing dead plants and adding them to the compost. Plant cover crops to improve soil health over winter.",
        "October": "Harvest the last of the crops and prepare the garden for winter. Mulch perennial plants to protect them from the cold. Plant spring bulbs like tulips and daffodils.",
        "November": "Finish any remaining garden cleanup. Protect tender plants from frost by moving them indoors or covering them. Check stored vegetables and fruits for spoilage.",
        "December": "Focus on indoor gardening activities like caring for houseplants or growing herbs on the windowsill. Review your garden plan and start preparing for the next growing season."
    }

    # Get static tips for the month
    static_tips = monthly_gardening_tips.get(month, "No specific tips available for this month.")

    # Conditional logic for specific months
    if month in ["October", "November", "December", "January", "February", "March", "April"]:
        weather_advice = "Do not plant outside, even if the weather seems warm. It's still too early for outdoor planting in Finland."
    else:
        weather_advice = "The weather seems suitable for outdoor planting. Follow the expert recommendations for planting and gardening activities."

    # Combine static tips and weather advice
    combined_tips = f"**Static Tips for {month}:**\n{static_tips}\n\n**Weather Considerations:**\n{weather_advice}"
    return combined_tips


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
    api_key = config.OPEN_WEATHER_MAP_API_KEY
    model_url = config.MODEL_URL
    print(system_prompt_weather)
    try:
        weather_data = test_openweathermap_api(api_key)
        next_3_hours_data = get_next_3_hours_data(weather_data)

        daily_forecast = translate_weather_data(next_3_hours_data)
        print("\nDaily Weather Forecast:")
        print(daily_forecast)

        current_month = datetime.now().strftime("%B")
        conditional_gardening_tips = get_conditional_gardening_tips(current_month, next_3_hours_data)
        dynamic_gardening_tips = gardening_tips(next_3_hours_data)
        print("\nConditional Gardening Tips:")
        print(conditional_gardening_tips)
        print("\nDynamic Gardening Tips:")
        print(dynamic_gardening_tips)

        # Generate audio files for the forecast and gardening tips
        text_to_speech(daily_forecast, filename='forecast.mp3')
        text_to_speech(dynamic_gardening_tips, filename='gardening_tips.mp3')

        # Save the results to a Markdown file
        with open('output.md', 'w') as file:
            file.write("# Daily Weather Forecast and Gardening Tips\n")
            file.write("## Date: " + datetime.now().strftime("%B %d, %Y") + "\n")
            file.write("\n## Weather Forecast\n")
            file.write(daily_forecast)
            file.write("\n## Gardening Tips\n")
            file.write(conditional_gardening_tips)
            file.write("\n## Dynamic Gardening Tips\n")
            file.write(dynamic_gardening_tips)

        # Define the embedded clock code
        clock_code = '<iframe src="https://indify.co/widgets/live/clock/mC6PDMEhkRcvdRHnRtuG" style="border:none;width:100%;height:100px;"></iframe>'

        # Save the results to an HTML file with the embedded clock code
        with open('index.html', 'w') as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html lang='en'>\n")
            file.write("<head>\n")
            file.write("    <meta charset='UTF-8'>\n")
            file.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
            file.write("    <title>Daily Weather Forecast and Gardening Tips</title>\n")
            file.write(
                "    <style> body { font-family: Arial, sans-serif; margin: 20px; } h1 { color: #2E8B57; } </style>\n")
            file.write("</head>\n")
            file.write("<body>\n")
            file.write("<h1>Daily Weather Forecast and Gardening Tips</h1>\n")
            file.write("<h2>Date: " + datetime.now().strftime("%B %d, %Y") + "</h2>\n")
            file.write(clock_code + "\n")
            file.write("<h3>Weather Forecast</h3>\n")
            file.write("<p>" + daily_forecast.replace('\n', '<br>') + "</p>\n")
            file.write("<h3>Gardening Tips</h3>\n")
            file.write("<p>" + conditional_gardening_tips.replace('\n', '<br>') + "</p>\n")
            file.write("<h3>Dynamic Gardening Tips</h3>\n")
            file.write("<p>" + dynamic_gardening_tips.replace('\n', '<br>') + "</p>\n")
            file.write("<h3>Current Time</h3>\n")
            file.write("</body>\n")
            file.write("</html>")

        # Commit and push changes
        commit_and_push_changes()

    except Exception as e:
        print(f"Failed to retrieve or translate weather data: {str(e)}")


if __name__ == "__main__":
    main()

