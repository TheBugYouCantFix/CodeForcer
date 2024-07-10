import csv
import os

from src.contracts.student_data import StudentData


def parse_students_data(path: str) -> list[StudentData]:
    extension = os.path.splitext(path)[-1]
    match extension:
        case ".csv":
            return __parse_students_data_from_csv(path)
        case _:
            pass  # TODO raise unsupported file extension exception


def __parse_students_data_from_csv(path: str) -> list[StudentData]:
    with open(path, mode='r') as file:
        csv_reader = csv.DictReader(file)

        return [
            StudentData(
                email=row['email'],
                handle=row['handle']
            ) for row in csv_reader
        ]
