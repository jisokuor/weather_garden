markdown
Kopioi koodi
# Weather Garden

Weather Garden is a web application that provides daily weather forecasts and gardening tips based on the weather data. The application fetches weather data from the OpenWeatherMap API and displays it along with gardening advice.

## Features

- Daily weather forecast
- Dynamic gardening tips based on weather
- Static gardening tips for the month of May
- Interactive weather forecast chart

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jisokuor/weather_garden.git
   cd weather_garden

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   
4. **Create a .env file in the project root directory and add your OpenWeatherMap API key:**
   ```bash
   OPENWEATHER_API_KEY=your_api_key_here

**Usage**

1. **Run the daily update script to fetch weather data and update gardening tips:**

   ```bash
   cmd.exe /c run_daily_update.bat
2. **Start the Flask server to serve the application:**

   ```bash
   python weatherforecast.py
3. **Open your web browser and navigate to:**
   ```bash
   http://127.0.0.1:5000/

**Environment Variables**

   **OPENWEATHER_API_KEY:** Your API key for accessing the OpenWeatherMap API.

**Technologies and Libraries**
 * Python: The main programming language.
 * Flask: A lightweight WSGI web application framework. 
 * Requests: A simple HTTP library for Python. 
 * BeautifulSoup4: A library for parsing HTML and XML documents. 
 * Matplotlib: A plotting library for the Python programming language. 
 * Dotenv: A library to load environment variables from a .env file.

 * Contributors
Jarkko Iso-Kuortti - Initial work
License
 * This project is licensed under the MIT License - see the LICENSE file for details.

