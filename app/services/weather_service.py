import requests
from fastapi import HTTPException
from services.get_geo_info import *


def get_env_variable(var_name: str) -> str:
    """Retrieve an environment variable and raise an error if it's not set."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"{var_name} not found in environment variables.")
    return value


class OpenWeatherService:
    """Service class for interacting with the OpenWeather API."""

    def __init__(self):
        self.openweather_api_key = get_env_variable("OPENWEATHER_API_KEY")
        self.current_weather_url = get_env_variable("CURRENT_WEATHER_URL")
        self.forecast_weather_url = get_env_variable("FORECAST_WEATHER_URL")
        self.history_weather_url = get_env_variable("HISTORY_WEATHER_URL")

    def fetch_weather_data(self, url, params):
        """Fetch weather data from the OpenWeather API."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve weather data: {str(e)}"
            )

    def get_weather_info(self, location, weather_type):
        """Retrieve weather information based on the query type."""

        locator = GeoLocation()

        try:
            latitude, longitude = locator.get_geo_info(location)
            print(
                f"The geolocation for {location} is Latitude: {latitude}, Longitude: {longitude}"
            )
        except ValueError as ve:
            print(ve)

        url_map = {
            "current": self.current_weather_url,
            "forecast": self.forecast_weather_url,
            "history": self.history_weather_url,
        }

        if weather_type not in url_map:
            raise ValueError(
                "Invalid query type. Must be 'current', 'forecast', or 'history'."
            )

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.openweather_api_key,
            "units": "metric",
        }

        # Additional parameter for the historical weather request
        if weather_type == "history":
            params["type"] = "hour"

        weather_data = self.fetch_weather_data(url_map[weather_type], params)
        return self._parse_weather_response(weather_data, location, weather_type)

    def _parse_weather_response(self, weather_data, location, weather_type):
        """Parse the weather data based on query type."""
        if weather_type == "current":
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            return f"The current weather in {location} is {description} with a temperature of {temperature}°C."

        elif weather_type == "forecast":
            forecast = weather_data["list"][0]
            timestamp = forecast["dt_txt"]
            description = forecast["weather"][0]["description"]
            temperature = forecast["main"]["temp"]
            return f"The weather forecast for {location} on {timestamp} is {description} with a temperature of {temperature}°C."

        elif weather_type == "history":
            history_data = weather_data["list"][0]
            description = history_data["weather"][0]["description"]
            temperature = history_data["main"]["temp"]
            return f"The weather in {location} was {description} with a temperature of {temperature}°C."
