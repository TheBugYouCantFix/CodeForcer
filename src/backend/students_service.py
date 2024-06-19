from contracts.student_data import StudentData
from domain.student import Student
from students_repository import IStudentsRepository


class StudentsService:
    students_repository: IStudentsRepository

    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def create_student(self, student_data: StudentData) -> Student:
        email = student_data.email
        handle = student_data.handle

        student = Student(email=email, handle=handle)

        self.students_repository.add_student(student)

        return student
