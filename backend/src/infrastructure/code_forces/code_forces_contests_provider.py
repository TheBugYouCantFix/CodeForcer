from domain.contest import Contest
from application.contests.contests_provider import IContestsProvider
from infrastructure.code_forces.code_forces_request_sender import CodeForcesRequestSender


class CodeForcesContestsProvider(IContestsProvider):
    def get_contest_results(self, contest_id: int, key: str, secret: str):
        request_sender = CodeForcesRequestSender(key, secret)
        _, _, rows = request_sender.contest_standings(contest_id)

        return [
            {"handle": row.party.members[0].handle, "result": row.points}
            for row in rows
        ]

    def get_contest(self, contest_id: int, key: str, secret: str) -> Contest:
        request_sender = CodeForcesRequestSender(key, secret)
        submissions = request_sender.contest_status(contest_id)
