from fastapi import APIRouter
from starlette import status

from .submission_selectors import submission_selectors

router = APIRouter()


@router.get("/contests/submission-selectors", status_code=status.HTTP_200_OK)
async def get_contests_submission_selectors() -> list[str]:
    return list(submission_selectors.keys())
