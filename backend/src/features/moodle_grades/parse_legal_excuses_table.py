from csv import DictReader
from datetime import timedelta, datetime
from os import path, remove

from fastapi import APIRouter, status, UploadFile, File, HTTPException
from pytz import timezone, utc
from pydantic import EmailStr

from src.features.moodle_grades.models import LegalExcuse

router = APIRouter()


@router.patch("/legal-excuses-file", status_code=status.HTTP_201_CREATED)
async def parse_legal_excuses_table(file: UploadFile = File(...)) -> dict[EmailStr, LegalExcuse]:
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb+") as file_object:
        file_object.write(file.file.read())

    legal_excuses = _parse_legal_excuses(file_path)

    if path.exists(file_path):
        remove(file_path)

    return legal_excuses


def _parse_legal_excuses(file_path: str) -> dict[EmailStr, LegalExcuse]:
    extension = path.splitext(file_path)[-1]
    match extension:
        case ".csv":
            return _parse_legal_excuses_from_csv(file_path)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file extension"
            )


def _parse_legal_excuses_from_csv(file_path: str) -> dict[EmailStr, LegalExcuse]:
    with open(file_path, mode='r', encoding=None) as file:
        csv_reader = DictReader(file)

        legal_excuses: dict[EmailStr, LegalExcuse] = {}

        for row in csv_reader:
            row: dict = row
            row = {
                key.lower().replace('-', '').replace('\'', ''): value
                for key, value
                in row.items()
            }

            email = row['email']

            absence_period_split = row['absence period'].split('-')
            start_time_utc = _parse_datetime(absence_period_split[0])

            if len(absence_period_split) == 1:
                duration = timedelta(days=1)
            else:
                end_time_utc = _parse_datetime(absence_period_split[1])
                duration = end_time_utc - start_time_utc

            legal_excuses[email] = LegalExcuse(start_time_utc=start_time_utc, duration=duration)

        return legal_excuses


def _parse_datetime(datetime_str: str) -> datetime:
    datetime_str = datetime_str.strip().strip('.')
    parsed_datetime = datetime.strptime(datetime_str, '%d.%m.%Y')

    return timezone("Europe/Moscow").localize(parsed_datetime, is_dst=None).astimezone(utc)
