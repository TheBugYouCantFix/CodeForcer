from fastapi import APIRouter
from starlette import status

from src.container import container
from src.features.contests.models import Contest
from src.features.contests.service import ContestsService

router = APIRouter()


@router.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_results(contest_id: int, key: str, secret: str):
    return container[ContestsService].get_contest_results(contest_id, key, secret)


@router.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(contest_id: int, key: str, secret: str) -> Contest:
    return container[ContestsService].get_contest(contest_id, key, secret)
