# engine/db.py

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "app.db"

def get_connection():
    return sqlite3.connect(DB_FILE)
