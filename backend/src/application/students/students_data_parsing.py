import csv

from contracts.student_data import StudentData


def parse_students_data(path: str) -> list[StudentData]:
    with open(path, mode='r') as file:
        csv_reader = csv.DictReader(file)

        return [
            StudentData(
                email=row['email'],
                handle=row['handle']
            ) for row in csv_reader
        ]
