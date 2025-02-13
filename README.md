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
   CURRENT_WEATHER_URL=current_weather_url
   FORECAST_WEATHER_URL=forecast_weather_url
   HISTORY_WEATHER_URL=history_weather_url
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

## Containerization with Docker

### Prerequisites

- Ensure Docker is installed and running on your machine.

### Steps for Docker

1. **Build Docker Image**

   Before building the image, ensure your `Dockerfile` is configured as described in the previous section.

   ```sh
   docker build -t weather-chatbot-api .
   ```

   This command builds and tags your Docker image as `weather-chatbot-api`.

2. **Run the Docker Container**

   You need to pass the environment variables defined in your `.env` file to the container. For that, use the `--env-file` option in the `docker run` command. Make sure your `.env` file is located in the same directory where you're running the command or provide the specific path to it.

   ```sh
   docker run -d --name weather-chatbot-api-container \
     --env-file .env \
     -p 8000:8000 \
     weather-chatbot-api
   ```

   This command runs the Docker container in detached mode (`-d`), sets the container name to `weather-chatbot-api-container`, exposes port 8000, and passes the environment variables.

3. **Access the API**

   Once the container is running, your FastAPI application will be accessible at `http://localhost:8000`.

4. **Stopping and Removing Containers**

   To stop the running container, use:

   ```sh
   docker stop weather-chatbot-api-container
   ```

   To remove the stopped container, use:

   ```sh
   docker rm weather-chatbot-api-container
   ```

#### Notes

- **Debugging**: If you encounter issues, check the logs of the container for debugging using:
  
  ```sh
  docker logs weather-chatbot-api-container
  ```

- **Environment Variables**: It's crucial to manage your sensitive environment variables (like API keys) securely. Consider using Docker Secrets or similar tools for production environments.

By following these steps, you can easily build and deploy this Weather Chatbot API within a Docker container, which simplifies deployment and scaling in different environments.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


## Additional Notes:
- Replace placeholder values such as `yourusername` or `your_openweather_api_key` with actual values where applicable.
- Ensure that any additional setup steps specific to your development environment (like database initialization) are documented accordingly.