from __future__ import annotations

from datetime import datetime

from src.features.contests.models import Contest

from pydantic import BaseModel, EmailStr, Field


class MoodleResultsData(BaseModel):
    contest: Contest
    problem_max_grade_by_index: dict[str, float]
    legal_excuses: dict[EmailStr, LegalExcuse]
    late_submission_policy: LateSubmissionPolicy
    submission_selector_name: str


class LateSubmissionPolicy(BaseModel):
    penalty: float = Field(ge=0, le=1)
    extra_time: int


class LegalExcuse(BaseModel):
    start_time_utc: datetime
    duration: int
