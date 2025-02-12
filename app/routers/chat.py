from fastapi import APIRouter, HTTPException
import json
from models.chat_model import UserInput, weather_context_analyzer
from services.weather_service import OpenWeatherService
from utils.langchain_integration import QueryProcessor
from database.db_manager import DatabaseManager

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request_data: UserInput):
    """
    Endpoint to process a chat query and return relevant weather information.

    Args:
        request_data (UserInput): Incoming query data in JSON format.

    Returns:
        dict: Dictionary containing the query and corresponding response.

    Raises:
        HTTPException: If no response is received from process_query.
    """
    query = request_data.user_query
    query_type = await analyze_weather_query(query)

    if query_type == "general query":
        response = await handle_general_query(query)
    else:
        response = await handle_weather_query(query_type)

    await save_query_response(query, response)
    return {query: response}


async def analyze_weather_query(query: str) -> str:
    """Analyze the query to determine if it's weather-related."""
    return weather_context_analyzer.invoke(query)


async def handle_general_query(query: str) -> str:
    """Process a general query and return a response."""
    processor = QueryProcessor()
    response = processor.process_query(query)

    if not response:
        raise HTTPException(
            status_code=500, detail="No response received from process_query."
        )

    return response


async def handle_weather_query(query_type: str) -> str:
    """Fetch and return weather information based on the analysis result."""
    query_data = json.loads(query_type)
    location = query_data["location"]
    weather_type = query_data["weather_type"]

    weather_service = OpenWeatherService()
    return weather_service.get_weather_info(location, weather_type)


async def save_query_response(query: str, response: str):
    """Save the processed query and its response to the database."""
    db_manager = DatabaseManager()
    db_manager.save_to_db(query, response)
