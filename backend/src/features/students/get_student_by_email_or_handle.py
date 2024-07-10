from email_validator import validate_email
from fastapi import HTTPException
from starlette import status

from src.container import container
from .interfaces import IStudentsRepository
from .model import Student
from . import router


@router.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str) -> Student:
    return GetStudentByEmailOrHandleCommandHandler(
        container[IStudentsRepository]
    ).handle(email_or_handle)


class GetStudentByEmailOrHandleCommandHandler:
    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def handle(self, email_or_handle: str) -> Student:
        if validate_email(email_or_handle):
            response = self.students_repository.get_student_by_email(email_or_handle)

            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Student with given email is not found'
                )
        else:
            response = self.students_repository.get_student_by_handle(email_or_handle)

            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Student with given handle is not found'
                )

        return response
