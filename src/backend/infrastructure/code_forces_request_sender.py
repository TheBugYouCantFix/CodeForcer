from random import randint
from hashlib import sha512
from time import time
from requests import get
import json
from domain.standings_fields import *
from domain.contest import Contest
from domain.problem import Problem


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
            problems: [Problem]
            rows: [RankListRow]

        result_data = self.send_request(method_name="contest.standings", contest_id=contest_id)

        contest = Contest(**result_data['contest'])
        problems = [Problem(**problem) for problem in result_data['problems']]
        rows = [RankListRow(**row) for row in result_data['rows']]

        result = Result(contest=contest, problems=problems, rows=rows)

        extracted_results = [
            {"handle": row.party.members[0].handle, "result": row.points}
            for row in result.rows
        ]

        return json.dumps(extracted_results)

