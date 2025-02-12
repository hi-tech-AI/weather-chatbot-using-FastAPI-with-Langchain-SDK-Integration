import re
from typing import Optional
from pydantic import BaseModel
from langchain_core.tools import tool


class UserInput(BaseModel):
    user_query: str


class WeatherAnalysisResult(BaseModel):
    location: str
    weather_type: str


@tool
def weather_context_analyzer(context: str) -> Optional[str]:
    """
    Analyze whether the input context is related to asking about weather for a specific city.

    Args:
        context (str): The input text to analyze

    Returns:
        str: A JSON string representing a WeatherAnalysisResult with location and weather type, or 'general query' if not a weather-related query.
    """
    # Expanded regex patterns to detect weather-related queries
    weather_patterns = [
        r"(?i)(want to know the weather of|weather of|current weather of|weather in)\s+([A-Za-z\s]+)(?:\s*right now| today| currently)?\??",
        r"(?i)(what\'?s?\s+the\s+(current|today\'?s?)\s+weather\s+in)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+forecast\s+for)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+in)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+history\s+of)\s+([A-Za-z\s]+)\??",
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, context, re.IGNORECASE)
        if match:
            weather_type = "current"

            if "forecast" in context.lower():
                weather_type = "forecast"
            elif "history" in context.lower():
                weather_type = "history"

            location = None
            for group in reversed(match.groups()):
                if group:
                    clean_location = re.sub(
                        r"\s*(right now|today|currently)\s*",
                        "",
                        group,
                        flags=re.IGNORECASE,
                    ).strip()
                    if clean_location:
                        location = clean_location
                        break

            if location:
                result = WeatherAnalysisResult(
                    location=location, weather_type=weather_type
                )
                return result.model_dump_json()

    return "general query"
