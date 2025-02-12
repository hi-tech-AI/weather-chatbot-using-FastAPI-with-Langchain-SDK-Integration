# Weather Chatbot API

A scalable FastAPI application that serves as a chatbot to process user inquiries about the weather. It leverages Langchain SDK for natural language processing and interacts with the OpenWeather API for fetching up-to-date weather data.

## Features

- **Chat Endpoint**: Allows users to interact via `/api/chat`, delivering weather information based on user queries.
- **Weather-related Queries**: Supports current weather, forecast, and historical data inquiries.
- **Integration with External APIs**: Utilizes OpenWeather API for accurate weather information.

## Installation

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management (optional)
- Docker (for containerization, optional)

### Steps

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/weather-chatbot-api.git
   cd weather-chatbot-api
   ```

2. **Create a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   Create a `.env` file with necessary configurations:

   ```
   OPENWEATHER_API_KEY=your_openweather_api_key
   OPENCAGE_API_KEY=your_opencage_api_key
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=your_langsmith_project_name
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the application**

   ```sh
   uvicorn main:app --reload
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

## Usage

### API Endpoints

- **POST** `/api/chat`  

  Takes user input and returns the processed query result related to weather information.

  **Request Example**:

  ```json
  {
    "user_query": "What is the weather like in New York today?"
  }
  ```

  **Response Example**:

  ```json
  {
    "What is the weather like in New York today?": "The current weather in New York is clear sky with a temperature of 18°C."
  }
  ```

## Development

### Run Tests

(Assuming tests are located in a `tests` folder)

```sh
pytest tests
```

### Linting and Code Quality

Use tools like `flake8` and `black` for linting and code formatting:

```sh
flake8 .
black .
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

### Additional Notes:
- Replace placeholder values such as `yourusername` or `your_openweather_api_key` with actual values where applicable.
- Ensure that any additional setup steps specific to your development environment (like database initialization) are documented accordingly.
- If using Docker, you might consider adding Docker-specific installation and running instructions.