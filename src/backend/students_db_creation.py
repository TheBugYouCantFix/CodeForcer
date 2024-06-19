import sqlite3
from db_context import DBContext

def create_students_db() -> None:
    db_context = DBContext('studens.db')
    db_context.execute_command("""
        CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        handle TEXT
    );
    """)
    db_context.commit()

