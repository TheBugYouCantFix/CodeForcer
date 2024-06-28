from random import randint
from hashlib import sha512
from time import time
from requests import get

from infrastructure.code_forces.models import *


class CodeForcesRequestSender:
    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def contest_standings(self, contest_id: int) -> tuple[CfContest, list[CfProblem], list[CfRankListRow]]:
        response = self.__send_request(method_name="contest.standings", contestId=contest_id)

        contest = get_contest_from_data(response['contest'])
        problems = [get_problems_from_data(problem_data) for problem_data in response['problems']]
        rows = [get_rank_list_row_from_data(row) for row in response['rows']]

        return contest, problems, rows

    def contest_status(self, contest_id: int) -> list[CfSubmission]:
        response = self.__send_request(method_name="contest.status", contestId=contest_id)

        submissions_data = response
        for submission_data in submissions_data:
            problem_data = submission_data['problem']

    def __send_request(self, method_name: str, **params: int | str | bool):
        rand = randint(100_000, 1_000_000 - 1)
        hasher = sha512()

        params["time"] = int(time())
        params["apiKey"] = self.key

        params_str = '&'.join(sorted(f"{p[0]}={p[1]}" for p in params.items()))

        hasher.update(f"{rand}/{method_name}?{params_str}#{self.secret}".encode())
        api_sig = str(rand) + hasher.hexdigest()

        resp = get(f"https://codeforces.com/api/{method_name}", params | {"apiSig": api_sig})

        if resp.status_code != 200:
            return None

        return resp.json()["result"]


def get_contest_from_data(contest_data: dict) -> CfContest:
    contest_data['type'] = CfContestType[contest_data['type']]
    contest_data['phase'] = CfPhase[contest_data['phase']]

    return CfContest(**contest_data)


def get_problems_from_data(problem_data: dict) -> CfProblem:
    problem_data['type'] = CfProblemType[problem_data['type']]
    return CfProblem(**problem_data)


def get_rank_list_row_from_data(rank_list_row_data: dict) -> CfRankListRow:
    rank_list_row_data['party']['participantType'] = CfParticipantType[rank_list_row_data['party']['participantType']]

    rank_list_row_data['problemResults'] = [
        int(problem_results_data['points'])
        for problem_results_data
        in rank_list_row_data['problemResults']
    ]

    rank_list_row_data['party']['members'] = [
        CfMember(**member)
        for member
        in rank_list_row_data['party']['members']
    ]

    rank_list_row_data['party'] = CfParty(**rank_list_row_data['party'])
    return CfRankListRow(**rank_list_row_data)


__all = ["CodeForcesRequestSender"]
