from fastapi import APIRouter
from starlette import status

from src.features.moodle_grades.submission_selectors import submission_selectors, submission_selectors_descriptions
from src.utils.name_end_description import NameAndDescription

router = APIRouter()


@router.get("/submission-selectors", status_code=status.HTTP_200_OK)
async def get_submission_selectors() -> list[NameAndDescription]:
    return [
        NameAndDescription(name=name, description=description)
        for name, description
        in zip(submission_selectors, submission_selectors_descriptions.values())
    ]
