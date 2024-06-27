from application.contests.contests_provider import IContestsProvider
from infrastructure.code_forces.code_forces_request_sender import CodeForcesRequestSender
from results_scrapping_fields.standings_fields import *


class CodeForcesContestsProvider(IContestsProvider):
    def get_contest_results(self, contest_id: int, key: str, secret: str):
        request_sender = CodeForcesRequestSender(key, secret)
        return scrap_results(request_sender, contest_id)

    def get_contest(self, contest_id: int, key: str, secret: str) -> Contest:
        pass #This has to be implemented


def scrap_results(request_sender: CodeForcesRequestSender, contest_id: int):
    result = request_sender.contest_standings(contest_id)

    extracted_results = [
        {"handle": row.party.members[0].handle, "result": row.points}
        for row in result.rows
    ]

    return extracted_results
