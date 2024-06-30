from infrastructure.storage.db_context import DBContext


def ensure_students_db_is_created(db_context: DBContext) -> None:
    db_context.execute_command("""
            CREATE TABLE IF NOT EXISTS students (
            email TEXT PRIMARY KEY,
            handle TEXT
        );
        """)
    db_context.commit()
