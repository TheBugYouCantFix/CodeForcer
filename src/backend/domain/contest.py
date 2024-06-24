from pydantic import BaseModel, EmailStr

from domain.enums.phase import Phase
from domain.enums.verdict import Verdict


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
    author_email: EmailStr
    verdict: Verdict
    passed_test_count: int
    points: int
    programming_language: str
