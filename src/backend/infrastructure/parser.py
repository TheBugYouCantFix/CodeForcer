import csv
from typing import List
from contracts.student_data import StudentData

def parse_csv(file_path: str) -> List[StudentData]:
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        students = []
        for row in csv_reader:
            students.append(StudentData(email=row['email'], handle=row['handle']))
    return students