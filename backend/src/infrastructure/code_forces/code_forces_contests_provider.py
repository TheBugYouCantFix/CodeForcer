from collections import defaultdict

from infrastructure.code_forces.code_forces_request_sender import CodeForcesRequestSender
from application.contests.contests_provider import IContestsProvider
from domain.contest import *


class CodeForcesContestsProvider(IContestsProvider):
    def get_contest_results(self, contest_id: int, api_key: str, api_secret: str):
        request_sender = CodeForcesRequestSender(api_key, api_secret)

        _, _, rows = request_sender.contest_standings(contest_id)

        return [
            {"handle": row.party.members[0].handle, "result": row.points}
            for row in rows
        ]

    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        request_sender = CodeForcesRequestSender(api_key, api_secret)

        cf_submissions = request_sender.contest_status(contest_id)
        cf_contest, cf_problems, _ = request_sender.contest_standings(contest_id)

        submissions_by_problem_index = defaultdict(list)
        for cf_submission in cf_submissions:
            problem_index = cf_submission.problem.index
            submission = Submission(
                id=cf_submission.id,
                author=ContestParticipant(
                    handle=cf_submission.author.members[0].handle
                ),
                verdict=cf_submission.verdict.value,
                passed_test_count=cf_submission.passedTestCount,
                points=cf_submission.points,
                programming_language=cf_submission.programmingLanguage
            )
            submissions_by_problem_index[problem_index].append(submission)

        problems = [
            Problem(
                index=cf_problem.index,
                name=cf_problem.name,
                max_points=cf_problem.points,
                submissions=submissions_by_problem_index[cf_problem.index]
            ) for cf_problem in cf_problems
        ]

        return Contest(
            id=contest_id,
            name=cf_contest.name,
            phase=cf_contest.phase.value,
            problems=problems
        )
