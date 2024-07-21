from __future__ import annotations

import csv
from enum import Enum
from io import StringIO
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import status, APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.utils.timed_event import TimedEvent
from src.features.contests.models import Problem, Submission
from .models import MoodleResultsData, LegalExcuse, LateSubmissionPolicy
from .submission_selectors import submission_selectors, submission_selector

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_grades_file(results_data: MoodleResultsData) -> StreamingResponse:
    filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    file = handle_create_grades_file(results_data)

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


def handle_create_grades_file(results_data: MoodleResultsData) -> StringIO:
    student_grade_map: defaultdict[str, list[float | str]] = defaultdict(lambda: [0, ''])

    file = StringIO()
    writer = csv.writer(file)

    contest = results_data.contest

    @submission_selector('absolute best')
    def absolute_best_submission_selector(submissions: list[Submission]) -> Submission:
        return max(submissions, key=lambda submission: calculate_points(results_data, submission)[0])

    contest.select_single_submission_for_each_participant(
        submission_selectors[results_data.submission_selector_name]
    )

    mark_grades(results_data.contest.problems, student_grade_map, results_data)

    writer.writerow(['Email', f'{contest.name} Grade', f'{contest.name} Feedback'])
    write_grades_to_file(writer, student_grade_map)

    return file


def mark_grades(
        problems: list[Problem],
        student_grade_map: defaultdict[str, list[float | str]],
        results_data: MoodleResultsData
) -> None:
    for problem in problems:
        update_grades(problem, student_grade_map, results_data)


def update_grades(
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
        grade, submission_time_type = calculate_grade(results_data, submission, max_grade, problem.max_points)

        comment = get_comment_from_submission_time_type(
            submission_time_type,
            results_data.late_submission_policy.penalty
        )

        feedback = f"Problem {problem.index}: {grade} {comment}\n\n"

        student_grade_map[submission.author.email][0] += grade
        student_grade_map[submission.author.email][1] += feedback


def calculate_grade(
        results_data: MoodleResultsData,
        submission: Submission,
        max_grade: float,
        max_points: float,
) -> (float, SubmissionTimeType):
    points, submission_time_type = calculate_points(
        results_data,
        submission
    )

    grade = points / max_points * max_grade

    return grade, submission_time_type


def calculate_points(
        results_data: MoodleResultsData,
        submission: Submission
) -> (float, SubmissionTimeType):
    legal_excuse = results_data.legal_excuses.get(submission.author.email)
    deadline_offset = get_deadline_offset(legal_excuse, results_data.contest)
    deadline = results_data.contest.end_time_utc + deadline_offset

    points, submission_time_type = apply_late_submission_policy(
        submission,
        deadline,
        results_data.late_submission_policy,
    )

    return points, submission_time_type


def apply_late_submission_policy(
        submission: Submission,
        deadline: datetime,
        late_submission_policy: LateSubmissionPolicy
) -> (float, SubmissionTimeType):
    extra_time = timedelta(seconds=late_submission_policy.extra_time)
    penalty = late_submission_policy.penalty

    submission_time_utc = submission.submission_time_utc
    late_submission_deadline = deadline + extra_time

    if submission_time_utc > late_submission_deadline:
        return 0.0, SubmissionTimeType.AFTER_LATE_SUBMISSION_POLICY

    if submission_time_utc > deadline:
        return submission.points * (1 - penalty), SubmissionTimeType.LATE_SUBMISSION_POLICY

    return submission.points, SubmissionTimeType.IN_TIME


def get_deadline_offset(legal_excuse: LegalExcuse | None, contest: TimedEvent) -> timedelta:
    if legal_excuse is not None and legal_excuse.intersects_with(contest):
        return legal_excuse.end_time_utc - max(contest.start_time_utc, legal_excuse.start_time_utc)

    return timedelta(0)


def get_comment_from_submission_time_type(submission_time_type: SubmissionTimeType, penalty: float) -> str:
    match submission_time_type:
        case SubmissionTimeType.IN_TIME:
            return ""
        case SubmissionTimeType.LATE_SUBMISSION_POLICY:
            return f"(Late submission policy applied: {penalty * 100}% grade reduction)"
        case SubmissionTimeType.AFTER_LATE_SUBMISSION_POLICY:
            return "(Submitted after the deadline)"

    return ""


def write_grades_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
    for email, (grade, feedback) in student_grade_map.items():
        writer.writerow([email, grade, feedback])


class SubmissionTimeType(Enum):
    IN_TIME = 0
    LATE_SUBMISSION_POLICY = 1
    AFTER_LATE_SUBMISSION_POLICY = 2
