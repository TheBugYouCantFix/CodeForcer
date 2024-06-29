from pydantic import BaseModel

from domain.enums import Phase, Verdict
from domain.student import ContestParticipant


class Contest(BaseModel):
    id: int
    name: str
    phase: Phase
    problems: list["Problem"]


class Problem(BaseModel):
    index: str
    name: str
    max_points: int
    submissions: list["Submission"]


class Submission(BaseModel):
    id: int
    author: ContestParticipant
    verdict: Verdict
    passed_test_count: int
    points: float | None
    programming_language: str
