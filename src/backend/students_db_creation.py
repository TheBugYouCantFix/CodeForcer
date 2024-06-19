from db_context import DBContext


def create_students_db() -> None:
    db_context = DBContext('students.db')
    db_context.execute_command("""
        CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        handle TEXT
    );
    """)
    db_context.commit()
