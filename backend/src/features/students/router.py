from fastapi import APIRouter, UploadFile, File
from starlette import status
from starlette.responses import Response

from src.container import container
from src.features.students.model import Student
from src.features.students.service import StudentsService

router = APIRouter()


@router.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: Student) -> Student | None:
    return container[StudentsService].create_student(student)


@router.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students() -> list[Student]:
    return container[StudentsService].get_all_students()


@router.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str) -> Student:
    return container[StudentsService].get_student_by_email_or_handle(email_or_handle)


@router.put("/students/{email}")
async def update_or_create_student(email: str, updated_student: Student, response: Response) -> Student | None:
    result = container[StudentsService].update_or_create_student(email, updated_student)

    if result is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None

    response.status_code = status.HTTP_201_CREATED
    return result


@router.put("/students/file", status_code=status.HTTP_201_CREATED)
async def update_or_create_students_from_file(file: UploadFile = File(...)) -> list[Student]:
    return container[StudentsService].update_or_create_students_from_file(file)


@router.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str) -> None:
    container[StudentsService].delete_student(email)
