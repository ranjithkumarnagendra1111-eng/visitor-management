import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # For dict-like access
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: tuple = ()):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    def fetch_all(self, query: str, params: tuple = ()):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    def fetch_one(self, query: str, params: tuple = ()):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

def init_db(db_path: Path):
    """Initialize the database with tables."""
    db = DatabaseManager(db_path)
    try:
        # Create employees table
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                role TEXT
            )
        """)

        # Create visitors table
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY,
                visitorName TEXT NOT NULL,
                company TEXT,
                purpose TEXT,
                checkInTime TEXT,
                checkOutTime TEXT,
                hostEmployeeId INTEGER,
                FOREIGN KEY (hostEmployeeId) REFERENCES employees(id)
            )
        """)

        # Create visits table (for visit history)
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY,
                visitor_id INTEGER,
                employee_id INTEGER,
                check_in_time TEXT,
                check_out_time TEXT,
                purpose TEXT,
                FOREIGN KEY (visitor_id) REFERENCES visitors(id),
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)

        logger.info("Database initialized successfully.")
    finally:
        db.close()