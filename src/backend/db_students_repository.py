from pydantic import EmailStr
from domain.student import Student
from students_repository import IStudentRepository
from db_context import DBContext


class DBStudentRepository(IStudentRepository):
    def __init__(self, db_name: str) -> None:
        self.db_context = DBContext(db_name)

    def add_student(self, student: Student):
        self.db_context.execute_command(
   "INSERT INTO students(email, handle) VALUES (?, ?)",
            (student.email, student.handle)
        )
        self.db_context.commit()

    def get_student_by_email(self, email: EmailStr) -> Student:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE email = ?",
            (email,)
        ).fetchone()

        if not result:
            print(f"Student with email {email} not found")
            return None

        return Student(result[0], result[1])

    def get_student_by_handle(self, handle: str) -> Student:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE handle = ?",
            (handle,)
        ).fetchone()

        if not result:
            print(f"Student with handle {handle} not found")
            return None

        return Student(result[0], result[1])

    def update_user(self, email: EmailStr, new_student: Student) -> None:
        self.db_context.execute_command(
            "UPDATE students SET email = ?, handle = ? WHERE email = ?",
            (new_student.email, new_student.handle, email)
        )
        self.db_context.commit()

    def delete_user(self, email: EmailStr) -> None:
        self.db_context.execute_command(
            "DELETE FROM students WHERE email = ?",
            (email,)
        )
        self.db_context.commit()

