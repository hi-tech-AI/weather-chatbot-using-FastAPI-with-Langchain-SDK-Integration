import requests
from fastapi import HTTPException
from services.geoinfo import *

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("Missing OpenWeather API Key")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_WEATHER_URL = "https://pro.openweathermap.org/data/2.5/forecast/hourly"
HISTORY_WEATHER_URL = "https://history.openweathermap.org/data/2.5/history/city"


def fetch_weather_data(url, params):
    """Fetch weather data from the OpenWeather API."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to retrieve weather data: {str(e)}"
        )


def get_weather_info(location, query_type):
    """Retrieve weather information based on the query type."""
    latitude, longitude = get_geo_info(location)

    if query_type not in ["current", "forecast", "history"]:
        raise ValueError(
            "Invalid query type. Must be 'current', 'forecast', or 'history'."
        )

    # Define base parameters
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    if query_type == "history":
        params["type"] = "hour"

    url_map = {
        "current": CURRENT_WEATHER_URL,
        "forecast": FORECAST_WEATHER_URL,
        "history": HISTORY_WEATHER_URL,
    }

    weather_data = fetch_weather_data(url_map[query_type], params)

    # Handle current weather response
    if query_type == "current":
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        return f"The current weather in {location} is {description} with a temperature of {temperature}°C."

    # Handle forecast response
    elif query_type == "forecast":
        forecast = weather_data["list"][0]
        timestamp = forecast["dt_txt"]
        description = forecast["weather"][0]["description"]
        temperature = forecast["main"]["temp"]
        return f"The weather forecast for {location} on {timestamp} is {description} with a temperature of {temperature}°C."

    # Handle historical weather response
    elif query_type == "history":
        history_data = weather_data["list"][0]
        description = history_data["weather"][0]["description"]
        temperature = history_data["main"]["temp"]
        return f"The weather in {location} was {description} with a temperature of {temperature}°C."
