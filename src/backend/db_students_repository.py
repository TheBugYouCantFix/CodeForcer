from pydantic import EmailStr
from domain.student import Student
from students_repository import IStudentsRepository
from db_context import DBContext


class DBStudentsRepository(IStudentsRepository):
    def __init__(self, db_name: str) -> None:
        self.db_context = DBContext(db_name)

    def add_student(self, student: Student):
        self.db_context.execute_command(
            "INSERT INTO students(email, handle) VALUES (?, ?)",
            (student.email, student.handle)
        )
        self.db_context.commit()

    def get_student_by_email(self, email: EmailStr) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE email = ?",
            email
        ).fetchone()

        if not result:
            print(f"Student with email {email} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def get_student_by_handle(self, handle: str) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE handle = ?",
            handle
        ).fetchone()

        if not result:
            print(f"Student with handle {handle} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def update_user(self, email: EmailStr, new_student: Student) -> None:
        self.db_context.execute_command(
            "UPDATE students SET email = ?, handle = ? WHERE email = ?",
            (new_student.email, new_student.handle, email)
        )
        self.db_context.commit()

    def delete_user(self, email: EmailStr) -> None:
        self.db_context.execute_command(
            "DELETE FROM students WHERE email = ?",
            email
        )
        self.db_context.commit()
