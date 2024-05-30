﻿# Weather Garden

Welcome to the Weather Garden project! This repository contains code and resources for providing daily weather updates and gardening tips.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Weather Garden project aims to provide users with daily weather forecasts and gardening tips. This can help gardeners plan their activities according to the weather conditions.

## Features
- **Daily Weather Updates**: Get accurate weather forecasts for your location.
- **Gardening Tips**: Receive helpful gardening tips tailored to the current weather.
- **Audio Forecasts**: Listen to weather forecasts and gardening tips in MP3 format.
- **Web Interface**: Access weather updates and tips via a web interface.

## Installation
To get started with the Weather Garden project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/jisokuor/weather_garden.git
    cd weather_garden
    ```

2. Set up a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To use the Weather Garden project, follow these steps:

1. Run the main script to get daily updates:
    ```sh
    python main.py
    ```

2. Access the web interface by opening `index.html` in your web browser.

## Project Structure
The project structure is organized as follows:

weather_garden/
│
├── Lib/
│ └── site-packages/ # External packages
│
├── Scripts/ # Helper scripts
│
├── forecast.mp3 # Audio file for weather forecast
├── gardening_tips.mp3 # Audio file for gardening tips
├── index.html # Web interface
├── ollamamodels.py # Weather prediction model
├── openweather_api_test7.py # Test script for OpenWeather API
├── output.md # Markdown output file
├── README.md # Project overview
├── requirements.txt # List of dependencies
└── main.py # Main script


## Contributing
We welcome contributions to the Weather Garden project. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
    ```sh

