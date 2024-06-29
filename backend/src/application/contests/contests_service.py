from pydantic import EmailStr

from domain.contest import Contest
from application.students.students_repository import IStudentsRepository
from application.contests.contests_provider import IContestsProvider


class ContestsService:
    contests_provider: IContestsProvider
    students_repository: IStudentsRepository

    def __init__(self, contests_provider: IContestsProvider, students_repository: IStudentsRepository):
        self.contests_provider = contests_provider
        self.students_repository = students_repository

    def get_contest_results(self, contest_id: int, key: str, secret: str):
        return self.contests_provider.get_contest_results(contest_id, key, secret)

    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        contest = self.contests_provider.get_contest(contest_id, api_key, api_secret)

        contest.map_handles_to_emails(handle_to_email_mapper=self.__get_email_by_handle)

        return contest

    def __get_email_by_handle(self, handle) -> EmailStr | None:
        student = self.students_repository.get_student_by_handle(handle)
        return student.email if student is not None else None

