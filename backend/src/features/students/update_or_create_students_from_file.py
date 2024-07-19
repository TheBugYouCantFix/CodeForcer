from csv import DictReader
from os import path, remove

from fastapi import status, UploadFile, File, HTTPException, APIRouter

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from .interfaces import IStudentsRepository
from .update_or_create_student import UpdateOrCreateStudentCommandHandler
from .models import Student, UpdatedOrCreatedStudentsResponse

router = APIRouter()


@router.patch("/file", status_code=status.HTTP_201_CREATED)
async def update_or_create_students_from_file(file: UploadFile = File(...)) -> UpdatedOrCreatedStudentsResponse:
    return UpdateOrCreateStudentsFromFileCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(file)


class UpdateOrCreateStudentsFromFileCommandHandler:
    def __init__(self, students_repository: IStudentsRepository, contests_provider: IContestsProvider):
        self.students_repository = students_repository
        self.contests_provider = contests_provider

    def handle(self, file: UploadFile) -> UpdatedOrCreatedStudentsResponse:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        students = _parse_students_data(file_location)

        if path.exists(file_location):
            remove(file_location)

        updated = 0
        created = 0

        for student in students:
            result = UpdateOrCreateStudentCommandHandler(
                self.students_repository,
                self.contests_provider
            ).handle(student.email, student)

            if result is None:
                updated += 1
            else:
                created += 1

        return UpdatedOrCreatedStudentsResponse(updated=updated, created=created)


def _parse_students_data(file_path: str) -> list[Student]:
    extension = path.splitext(file_path)[-1]
    match extension:
        case ".csv":
            return _parse_students_data_from_csv(file_path)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file extension"
            )


def _parse_students_data_from_csv(file_path: str) -> list[Student]:
    with open(file_path, mode='r', encoding=None) as file:
        csv_reader = DictReader(file)

        return [
            Student(
                email=row['email'],
                handle=row['handle']
            ) for row in csv_reader
        ]
