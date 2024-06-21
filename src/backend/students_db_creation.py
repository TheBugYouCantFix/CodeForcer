from db_context import DBContext


def create_students_db(db_name: str) -> None:
    db_context = DBContext(db_name)
    db_context.execute_command("""
        CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        handle TEXT
    );
    """)
    db_context.commit()
