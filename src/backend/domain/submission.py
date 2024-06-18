from pydantic import BaseModel, EmailStr
from domain.enums.verdict import Verdict


class Submission(BaseModel):
    id: int
    contest_id: int
    problem_index: str
    author_email: EmailStr
    verdict: Verdict
    passed_test_count: int
    points: int
    programming_language: str
