import sqlite3

DATABASE = "weather_chat.db"


def init_db():
    """Initialize the database and create the weather_chat table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """
        )


def save_to_db(query, response):
    """Save the query and response to the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO weather_chat (query, response) VALUES (?, ?)",
            (query, response),
        )
