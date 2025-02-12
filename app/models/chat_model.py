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
        str: A JSON string representing a WeatherAnalysisResult with location and weather type,
             or 'general query' if not a weather-related query.
    """
    weather_patterns = compile_weather_patterns()

    for pattern in weather_patterns:
        match = parse_weather_pattern(pattern, context)
        if match:
            return create_analysis_result(match, context)

    return "general query"


def compile_weather_patterns() -> list:
    """Compile regex patterns to detect weather-related queries."""
    patterns = [
        r"(?i)(want to know the weather of|weather of|current weather of|weather in)\s+([A-Za-z\s]+)(?:\s*right now| today| currently)?\??",
        r"(?i)(what\'?s?\s+the\s+(current|today\'?s?)\s+weather\s+in)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+forecast\s+for)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+in)\s+([A-Za-z\s]+)\??",
        r"(?i)(weather\s+history\s+of)\s+([A-Za-z\s]+)\??",
    ]
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]


def parse_weather_pattern(pattern: re.Pattern, context: str) -> Optional[re.Match]:
    """Parse the given context string for a specific weather-related pattern."""
    return pattern.search(context)


def create_analysis_result(match: re.Match, context: str) -> str:
    """Create a WeatherAnalysisResult based on the matched pattern."""
    weather_type = determine_weather_type(context)
    location = extract_location(match)

    if location:
        result = WeatherAnalysisResult(location=location, weather_type=weather_type)
        return result.model_dump_json()

    return "general query"


def determine_weather_type(context: str) -> str:
    """Determine the type of weather information being queried."""
    lower_context = context.lower()
    if "forecast" in lower_context:
        return "forecast"
    if "history" in lower_context:
        return "history"
    return "current"


def extract_location(match: re.Match) -> Optional[str]:
    """Extract and clean the location from the regex match."""
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
    return location
