from __future__ import annotations

from typing import Callable
from pydantic import BaseModel, EmailStr

from domain.enums import Phase, Verdict
from domain.student import ContestParticipant, Student


class Contest(BaseModel):
    id: int
    name: str
    phase: Phase
    problems: list[Problem]

    def map_handles_to_emails(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        for problem in self.problems:
            problem.map_handles_to_emails(handle_to_email_mapper)

    def select_single_submission_for_each_student(self,
                                                  selector: Callable[[Submission, Submission], Submission]) -> None:
        for problem in self.problems:
            problem.select_single_submission_for_each_student(selector)

    @property
    def get_participants(self) -> set[ContestParticipant]:
        return {
            participant
            for problem in self.problems
            for participant in problem.get_participants
        }


class Problem(BaseModel):
    index: str
    name: str
    max_points: float | None
    submissions: list[Submission]

    def map_handles_to_emails(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        for submission in self.submissions:
            submission.map_author_handle_to_email(handle_to_email_mapper)

    def select_single_submission_for_each_student(self,
                                                  selector: Callable[[Submission, Submission], Submission]) -> None:
        selected_submissions: dict[str, Submission] = {}

        for submission in self.submissions:
            handle = submission.author.handle
            if handle not in selected_submissions.keys():
                selected_submissions[handle] = submission
            else:
                selected_submissions[handle] = selector(selected_submissions[handle], submission)

        self.submissions = list(selected_submissions.values())

    @property
    def get_participants(self) -> set[ContestParticipant]:
        return {submission.author for submission in self.submissions}


class Submission(BaseModel):
    id: int
    author: ContestParticipant
    verdict: Verdict
    passed_test_count: int
    points: float | None
    programming_language: str

    def map_author_handle_to_email(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        if isinstance(self.author, Student):
            return

        email = handle_to_email_mapper(self.author.handle)
        if email is not None:
            self.author = Student(
                handle=self.author.handle,
                email=email
            )
