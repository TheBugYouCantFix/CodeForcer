from fastapi import status

from src.features.contests.models import Contest
from src.features.students.interfaces import IStudentsRepository
from tests.create_test_client import client


def test_new(contest, students_repo_mock: IStudentsRepository):
    response = client.get(f"/contests/{contest.id}", params={"key": "", "secret": ""})

    assert response.status_code == status.HTTP_200_OK
    assert Contest.model_validate_json(response.text) == contest
