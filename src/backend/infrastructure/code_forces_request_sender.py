from random import randint
from hashlib import sha512
from time import time
from requests import get
import json
from results_scrapping_fields.standings_fields import *


class CodeForcesRequestSender:
    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def send_request(self, method_name: str, **params: int | str | bool) -> object | None:
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

    def scrap_results(self, contest_id: int):
        class Result(BaseModel):
            contest: Contest
            problems: list[Problem]
            rows: list[RankListRow]

            class Config:
                arbitrary_types_allowed = True

        result_data = self.send_request(method_name="contest.standings", contestId=contest_id)

        contest_data = result_data['contest']
        contest_data['type'] = ContestType[contest_data['type']]
        contest_data['phase'] = Phase[contest_data['phase']]

        contest = Contest(**contest_data)
        problems_data = result_data['problems']
        for problem in problems_data:
            problem['type'] = ProblemType[problem['type']]

        problems = [Problem(**problem) for problem in problems_data]

        # Process rows
        rows_data = result_data['rows']
        for row in rows_data:
            row['party']['participantType'] = ParticipantType[row['party']['participantType']]

            row['problemResults'] = [int(pr['points']) for pr in row['problemResults']]
            if 'lastSubmissionTimeSeconds' not in row:
                row['lastSubmissionTimeSeconds'] = 0

            row['party']['members'] = [Member(**member) for member in row['party']['members']]

        rows = [RankListRow(**row) for row in rows_data]

        result = Result(contest=contest, problems=problems, rows=rows)

        extracted_results = [
            {"handle": row.party.members[0].handle, "result": row.points}
            for row in result.rows
        ]

        return json.dumps(extracted_results)
