from fastapi import status

from src.features.contests.models import Contest
from tests.create_test_client import client


def test_gets_contest_when_contest_exists(contest, students_repo_mock):
    response = client.get(f"/contests/{contest.id}", params={"key": "", "secret": ""})

    assert response.status_code == status.HTTP_200_OK

    response_contest = Contest.model_validate_json(response.text)

    assert response_contest.id == contest.id
    assert response_contest.name == contest.name
    assert response_contest.start_time_utc == contest.start_time_utc
    assert response_contest.duration == contest.duration
    for response_problem in response_contest.problems:
        for problem in contest.problems:
            if problem.index == response_problem.index:
                break
        else:
            assert False, f"Problem with index {response_problem.index} not found in the original contest"

        assert response_problem.name == problem.name
        assert response_problem.max_points == problem.max_points
