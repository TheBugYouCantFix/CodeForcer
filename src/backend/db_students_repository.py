from fastapi import HTTPException, status
from pydantic import EmailStr
from domain.student import Student
from students_repository import IStudentsRepository
from db_context import DBContext
from students_db_creation import create_students_db


class DBStudentsRepository(IStudentsRepository):
    def __init__(self, db_name: str) -> None:
        create_students_db(db_name)
        self.db_context = DBContext(db_name)

    def email_exists(self, email: EmailStr) -> bool:
        return self.get_student_by_email(email) is not None

    def handle_exists(self, handle: str) -> bool:
        return self.get_student_by_handle(handle) is not None

    def student_exists(self, student: Student) -> bool:
        return self.email_exists(student.email) and self.handle_exists(student.handle)

    def add_student(self, student: Student) -> None:
        if self.email_exists(student.email):
            print(f"Student with email {student.email} already exists")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists")

        self.db_context.execute_command(
            "INSERT INTO students(email, handle) VALUES (?, ?)",
            (student.email, student.handle, )
        )
        self.db_context.commit()

    def get_student_by_email(self, email: EmailStr) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE email = ?",
            (email, )
        ).fetchone()

        if not result:
            print(f"Student with email {email} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def get_student_by_handle(self, handle: str) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE handle = ?",
            (handle, )
        ).fetchone()

        if not result:
            print(f"Student with handle {handle} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def update_user(self, email: EmailStr, new_student: Student) -> None:
        if not self.email_exists(email):
            raise HTTPException(status_code=400, detail="Student does not exist")

        self.db_context.execute_command(
            "UPDATE students SET email = ?, handle = ? WHERE email = ?",
            (new_student.email, new_student.handle, email, )
        )
        self.db_context.commit()

    def delete_user(self, email: EmailStr) -> None:
        if not self.email_exists(email):
            raise HTTPException(status_code=400, detail="Student does not exist")

        self.db_context.execute_command(
            "DELETE FROM students WHERE email = ?",
            (email, )
        )
        self.db_context.commit()
