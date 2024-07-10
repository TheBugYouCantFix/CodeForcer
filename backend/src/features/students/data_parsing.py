import csv
import os

from src.features.students.model import Student


def parse_students_data(path: str) -> list[Student]:
    extension = os.path.splitext(path)[-1]
    match extension:
        case ".csv":
            return __parse_students_data_from_csv(path)
        case _:
            pass  # TODO raise unsupported file extension exception


class StudentData:
    pass


def __parse_students_data_from_csv(path: str) -> list[Student]:
    with open(path, mode='r') as file:
        csv_reader = csv.DictReader(file)

        return [
            Student(
                email=row['email'],
                handle=row['handle']
            ) for row in csv_reader
        ]
