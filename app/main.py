import uvicorn
from fastapi import FastAPI
from routers.chat import router as chat_router
from database.db_manager import DatabaseManager


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI()
    app.include_router(chat_router, prefix="/api")
    return app


def initialize_database():
    """Initialize the database connection."""
    db_manager = DatabaseManager()
    db_manager.initialize_database()


def main():
    """Main entry point for running the application."""
    initialize_database()
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
