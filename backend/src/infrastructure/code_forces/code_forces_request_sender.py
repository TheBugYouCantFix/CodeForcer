from dataclasses import dataclass
from random import randint
from hashlib import sha512
from time import time
from requests import get

from results_scrapping_fields.standings_fields import *


class CodeForcesRequestSender:
    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def contest_standings(self, contest_id: int) -> tuple[CfContest, list[CfProblem], list[CfRankListRow]]:
        response = self.__send_request(method_name="contest.standings", contestId=contest_id)

        contest_data = response['contest']
        contest_data['type'] = CfContestType[contest_data['type']]
        contest_data['phase'] = CfPhase[contest_data['phase']]

        contest = CfContest(**contest_data)

        problems_data = response['problems']
        for problem in problems_data:
            problem['type'] = CfProblemType[problem['type']]

        problems = [CfProblem(**problem) for problem in problems_data]

        rows_data = response['rows']
        for row_data in rows_data:
            row_data['party']['participantType'] = CfParticipantType[row_data['party']['participantType']]

            row_data['problemResults'] = [
                int(problem_results_data['points'])
                for problem_results_data
                in row_data['problemResults']
            ]

            row_data['party']['members'] = [
                CfMember(**member)
                for member
                in row_data['party']['members']
            ]

            row_data['party'] = CfParty(**row_data['party'])

        rows = [CfRankListRow(**row) for row in rows_data]

        return contest, problems, rows

    def contest_status(self, contest_id: int):
        response = self.__send_request(method_name="contest.status", contestId=contest_id)
        # response is a list of submissions

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

