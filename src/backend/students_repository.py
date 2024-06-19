from abc import ABC, abstractmethod
from pydantic import BaseModel, EmailStr
from domain.student import Student


class IStudentRepository(ABC):
    @abstractmethod
    def add_student(self, student: Student):
        pass

    @abstractmethod
    def get_student_by_email(self, email: EmailStr) -> Student:
        pass

    @abstractmethod
    def get_student_by_handle(self, handle: str) -> Student:
        pass

    @abstractmethod
    def update_user(self, email: EmailStr, new_student: Student) -> None:
        pass

    @abstractmethod
    def delete_user(self, email: EmailStr) -> None:
        pass
