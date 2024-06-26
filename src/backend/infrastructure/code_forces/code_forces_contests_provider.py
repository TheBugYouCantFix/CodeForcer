from application.contests.contests_provider import IContestsProvider
from infrastructure.code_forces.code_forces_request_sender import CodeForcesRequestSender
from results_scrapping_fields.standings_fields import *


class CodeForcesContestsProvider(IContestsProvider):
    def get_contest(self, contest_id: int, key: str, secret: str):
        request_sender = CodeForcesRequestSender(key, secret)
        return scrap_results(request_sender, contest_id)


def scrap_results(request_sender: CodeForcesRequestSender, contest_id: int):
    class Result(BaseModel):
        contest: Contest
        problems: list[Problem]
        rows: list[RankListRow]

        class Config:
            arbitrary_types_allowed = True

    result_data = request_sender.send_request(method_name="contest.standings", contestId=contest_id)

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

    return extracted_results
