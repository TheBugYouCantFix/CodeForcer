from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr, Field


class MoodleResultsData(BaseModel):
    contest: ContestData
    legal_excuses: dict[EmailStr, LegallyExcusedStudentData]
    late_submission_policy: LateSubmissionPolicyData

    def __getitem__(self, email: EmailStr) -> LegallyExcusedStudentData | None:
        return self.legal_excuses.get(email)


class ContestData(BaseModel):
    id: int
    name: str
    start_time_utc: datetime
    duration: timedelta
    problems: list[ProblemData]


class ProblemData(BaseModel):
    name: str
    index: str
    max_points: int | None
    max_grade: int
    submissions: list[SubmissionData]


class SubmissionData(BaseModel):
    id: int
    author_email: EmailStr
    is_successful: bool
    passed_test_count: int
    points: int | None
    programming_language: str
    submission_time_utc: datetime


class LateSubmissionPolicyData(BaseModel):
    penalty: float = Field(ge=0, le=1)
    extra_time: int


class LegallyExcusedStudentData(BaseModel):
    email: EmailStr
    excuse_duration: int

