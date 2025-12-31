import sqlite3
import shutil
from pathlib import Path

DB_PATH = Path("app.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def backup_db():
    backup_path = DB_PATH.with_suffix(".backup.db")
    shutil.copy(DB_PATH, backup_path)
    return backup_path
