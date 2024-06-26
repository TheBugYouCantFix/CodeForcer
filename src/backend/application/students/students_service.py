from validate_email import validate_email
from fastapi import HTTPException, status, UploadFile

from domain.student import Student
from application.students.students_repository import IStudentsRepository
from contracts.student_data import StudentData
from infrastructure.parser import parse_csv


def student_data_to_student(student_data: StudentData) -> Student:
    email = student_data.email
    handle = student_data.handle

    return Student(email=email, handle=handle)


class StudentsService:
    students_repository: IStudentsRepository

    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def create_student(self, student_data: StudentData) -> Student:
        student = student_data_to_student(student_data)
        self.students_repository.add_student(student)

        return student

    def get_student_by_email_or_handle(self, email_or_handle: str) -> Student:
        if validate_email(email_or_handle):
            response = self.students_repository.get_student_by_email(email_or_handle)
        else:
            response = self.students_repository.get_student_by_handle(email_or_handle)

        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return response

    def update_student(self, email: str, updated_student_data: StudentData):
        student = student_data_to_student(updated_student_data)
        self.students_repository.update_student(email, student)

    def delete_student(self, email: str):
        self.students_repository.delete_student(email)

    def process_csv_file(self, file: UploadFile):
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        students_data = parse_csv(file_location)
        for student_data in students_data:
            self.create_student(student_data)
