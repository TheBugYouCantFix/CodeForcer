import csv
from io import StringIO
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import status, APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.features.contests.models import Problem, Submission
from .models import MoodleResultsData
from .submission_selectors import submission_selectors

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_grades_file(results_data: MoodleResultsData) -> StreamingResponse:
    filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    file = CreateGradesFileCommand().handle(results_data)

    content_length = len(file.getvalue())
    file.seek(0)

    return StreamingResponse(
        file,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Length': str(content_length),
        },
        media_type='text/csv'
    )


class CreateGradesFileCommand:
    def handle(self, results_data: MoodleResultsData) -> StringIO:
        student_grade_map: defaultdict[str, list[float | str]] = defaultdict(lambda: [0, ''])

        file = StringIO()
        writer = csv.writer(file)

        contest = results_data.contest
        contest.select_single_submission_for_each_participant(
            submission_selectors[results_data.submission_selector_name]
        )

        writer.writerow(['Email', f'{contest.name} Grade', f'{contest.name} Feedback'])

        self._mark_grades(results_data.contest.problems, student_grade_map, results_data)
        self._write_to_file(writer, student_grade_map)

        for _, feedback in student_grade_map.values():
            feedback += '"'

        return file

    def _mark_grades(
            self,
            problems: list[Problem],
            student_grade_map: defaultdict[str, list[float | str]],
            results_data: MoodleResultsData
    ) -> None:
        for problem in problems:
            self._update_grades(problem, student_grade_map, results_data)

    @staticmethod
    def _update_grades(
            problem: Problem,
            student_grade_map: defaultdict[str, list[float | str]],
            results_data: MoodleResultsData
    ) -> None:
        if problem.index not in results_data.problem_max_grade_by_index:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Problem {problem.index} has no max grade specified"
            )

        max_grade = results_data.problem_max_grade_by_index[problem.index]

        for submission in problem.submissions:
            if submission.points is None or problem.max_points is None:
                problem_points = CreateGradesFileCommand._get_grade_by_verdict(submission, max_grade)
            else:
                problem_points = submission.points / problem.max_points * max_grade

            problem_points, comment = CreateGradesFileCommand._apply_late_submission_policy(
                results_data,
                submission,
                problem_points
            )

            student_grade_map[submission.author.email][0] += problem_points

            comment = f"({comment})" if comment != "" else comment
            feedback = f"Problem {problem.index}: {problem_points} {comment}\n\n"
            if student_grade_map[submission.author_email][1] is not None:
                student_grade_map[submission.author_email][1] += feedback
            else:
                student_grade_map[submission.author_email][1] = '"' + feedback

    @staticmethod
    def _get_grade_by_verdict(submission: Submission, max_grade: float) -> float:
        return max_grade if submission.is_successful else 0

    @staticmethod
    def _apply_late_submission_policy(
            moodle_results_data: MoodleResultsData,
            submission: Submission,
            points: float
    ) -> (float, str):
        penalty = moodle_results_data.late_submission_policy.penalty
        legal_excuse = moodle_results_data.legal_excuses.get(submission.author.email)
        contest_start_time_utc = moodle_results_data.contest.start_time_utc
        contest_duration = moodle_results_data.contest.duration
        extra_time_seconds = moodle_results_data.late_submission_policy.extra_time
        submission_time = submission.submission_time_utc
        excuse_time_seconds = 0 if legal_excuse is None else legal_excuse.duration

        extra_time = timedelta(seconds=extra_time_seconds)
        excuse_time = timedelta(seconds=excuse_time_seconds)
        deadline_time = contest_start_time_utc + contest_duration + excuse_time

        deadline_time_extended = deadline_time + extra_time

        comment = ""
        if submission_time > deadline_time_extended:
            comment = "submitted after the deadline"
            return 0.0, comment

        if submission_time > deadline_time:
            comment = f"Late submission policy applied: {penalty * 100}% grade reduction"
            return points * (1 - penalty), comment

        return points, comment

    @staticmethod
    def _write_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email, (grade, feedback) in student_grade_map.items():
            writer.writerow([email, grade, feedback])
