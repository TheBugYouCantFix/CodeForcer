from fastapi import Response, HTTPException, status

from src.container import container
from .create_student import CreateStudentCommandHandler
from .interfaces import IStudentsRepository
from .model import Student
from . import router
from ..contests.interfaces import IContestsProvider


@router.put("/students/{email}")
async def update_or_create_student(email: str, updated_student: Student, response: Response) -> Student | None:
    result = UpdateOrCreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(email, updated_student)

    if result is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None

    response.status_code = status.HTTP_201_CREATED
    return result


class UpdateOrCreateStudentCommandHandler:
    def __init__(self, students_repository: IStudentsRepository, contests_provider: IContestsProvider):
        self.students_repository = students_repository
        self.contests_provider = contests_provider

    def handle(self, email: str, student: Student) -> Student | None:
        if email != student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email from URL should match email from reqeust body"
            )

        if not self.students_repository.email_exists(email):
            return CreateStudentCommandHandler(
                container[IStudentsRepository],
                container[IContestsProvider]
            ).handle(student)

        if not self.contests_provider.validate_handle(student.handle):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Handle does not belong to CodeForces user'
            )

        self.students_repository.update_student(email, student)
