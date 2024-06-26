from domain.contest import Contest
from application.contests.contests_provider import IContestsProvider


class ContestsService:
    contests_provider: IContestsProvider

    def __init__(self, contests_provider):
        self.contests_provider = contests_provider

    def get_contest_results(self, contest_id: int, key: str, secret: str):
        return self.contests_provider.get_contest_results(contest_id, key, secret)

    def get_contest(self, contest_id: int, key: str, secret: str) -> Contest:
        return self.contests_provider.get_contest(contest_id, key, secret)
