# Weather App

This repository contains a simple Weather application built using Python, `tkinter`, and the OpenWeather API. The app lets you search for a city and displays current weather plus a 5-day forecast, you can also click a day to view the forecast in 3-hour intervals.

## Overview

The Weather App provides a GUI where you can:
- Search a location by name
- View current conditions (temperature, humidity, wind, visibility, sunrise, sunset, chance of rain)
- View a 5-day forecast
- Click a forecast day to open a detailed screen with 3-hour interval data
- Move between forecast days using Next Day, Previous Day buttons

## Features

- **Current Weather**
  - Temperature
  - Condition description and icon
  - Humidity
  - Wind speed
  - Visibility
  - Min and max temperature
  - Sunrise and sunset
  - Chance of rain (when available)

- **5-Day Forecast**
  - Forecast cards for the next 5 days
  - Weather icons and midday temperatures

- **Detailed Forecast View**
  - 3-hour interval breakdown for a selected day
  - Navigation between available forecast days

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)
- OpenWeather API key (free tier is enough)

Python packages (installed via `requirements.txt`):
- `requests`
- `python-dotenv`
- `Pillow`
Open .env.example

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Myszanik/WeatherApp.git
2. **Navigate to the Project Directory**:
   ```bash
   cd WeatherApp
3. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv .venv
   ```
   ```bash
   .venv\Scripts\activate
4. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements.txt
5. **Add your OpenWeather API key**:  
	- Create a file named `.env` in the project folder (same level as `WeatherApp.py`)
   ```bash
   api_key=YOUR_OPENWEATHER_API_KEY
6. **Run the Application**:
   ```bash
   python WeatherApp.py

## Notes

- The `.env` file is intentionally not included in the repository, each user must create their own to run the app.
- If you make the repo public, your API key stays safe as long as `.env` is not committed.

## Acknowledgements

- `tkinter`, for the GUI
- OpenWeather API, for weather data
- `requests`, for HTTP requests
- `python-dotenv`, for loading environment variables from .env
- `Pillow`, for displaying weather icons

## Status

This project is for learning and practice. Improvements and clean-ups are welcome.




