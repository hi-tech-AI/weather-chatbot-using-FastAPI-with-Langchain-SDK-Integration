import sqlite3
from contextlib import contextmanager

DATABASE = "weather_chat.db"


class DatabaseManager:
    def __init__(self, db_file=DATABASE):
        self.db_file = db_file
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database and create the weather_chat table if it doesn't exist."""
        with self._get_connection() as conn:
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

    @contextmanager
    def _get_connection(self):
        """Context manager to handle database connection setup and teardown."""
        try:
            conn = sqlite3.connect(self.db_file)
            yield conn
        finally:
            conn.close()

    def save_to_db(self, query, response):
        """Save the query and response to the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO weather_chat (query, response) VALUES (?, ?)",
                    (query, response),
                )
                conn.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError("Failed to save data to the database.") from e
