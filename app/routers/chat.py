from fastapi import APIRouter, HTTPException
import json
from models.chat_model import UserInput, weather_context_analyzer
from services.weather_service import get_weather_info
from utils.langchain_integration import process_query
from database.db_manager import save_to_db

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
    query_type = weather_context_analyzer.invoke(query)

    if query_type == "general query":
        response = process_query(query)
        if not response:
            raise HTTPException(status_code=500, detail="No response received from process_query.")
        save_to_db(query, response)
        return {query: response}
    else:
        location = json.loads(query_type)["location"]
        weather_type = json.loads(query_type)["weather_type"]
        weather_info = get_weather_info(location, weather_type)
        save_to_db(query, weather_info)
        return {query: weather_info}
