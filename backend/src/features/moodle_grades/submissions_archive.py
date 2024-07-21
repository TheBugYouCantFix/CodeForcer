from __future__ import annotations

import os
import shutil
from datetime import datetime, timedelta
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from fastapi import APIRouter, status, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse

from src.features.contests.models import Contest, Submission
from src.features.moodle_grades.models import MoodleResultsData, LateSubmissionPolicy, LegalExcuse
from src.features.moodle_grades.submission_selectors import submission_selectors, submission_selector
from src.utils.timed_event import TimedEvent

router = APIRouter()


@router.post('/with-archive', status_code=status.HTTP_200_OK)
async def sort_submissions_archive(
        background_tasks: BackgroundTasks,
        results_data: str = Form(...),
        submissions_archive: UploadFile = File(...)
) -> FileResponse:
    results_data = MoodleResultsData.model_validate_json(results_data)

    contest = results_data.contest

    @submission_selector('absolute best',
                         'selects the best submission, takes late submission policy and legal excuses into account')
    def absolute_best_submission_selector(submissions: list[Submission]) -> Submission:
        return max(submissions, key=lambda submission: calculate_points(results_data, submission))

    contest.select_single_submission_for_each_participant(
        submission_selectors[results_data.submission_selector_name]
    )

    await handle_sort_submissions_archive(contest, submissions_archive)
    os.rename(
        f'features/moodle_grades/submissions_temp/{contest.id}.zip',
        f'features/moodle_grades/submissions_temp/{contest.name}.zip'
    )

    temp_folder = 'features/moodle_grades/submissions_temp'
    filepath = f'{temp_folder}/{contest.name}.zip'
    response = FileResponse(filepath, filename=f'{contest.name}.zip')

    background_tasks.add_task(shutil.rmtree, temp_folder)

    return response


async def handle_sort_submissions_archive(contest: Contest, submissions_archive: UploadFile = File(...)) -> ZipFile:
    archive_bytes = await submissions_archive.read()

    with ZipFile(BytesIO(archive_bytes), 'r') as zip_ref:
        zip_ref.extractall('features/moodle_grades/submissions_temp/extracted_files')
        submission_ids = zip_ref.namelist()
        create_result_folder(contest, submission_ids)

    return create_result_zip_file(contest.id)


def create_result_folder(contest: Contest, submission_ids: list[str]):
    create_problem_folders(contest)
    fill_problem_folders(contest, submission_ids)


def fill_problem_folders(contest: Contest, submission_file_names: list[str]):
    parent_dir = f'features/moodle_grades/submissions_temp/{contest.id}'
    for problem in contest.problems:
        problem_path = os.path.join(parent_dir, f'{problem.name} {problem.index}')

        for submission_file_name in submission_file_names:
            submission_id = int(get_file_name_without_extension(submission_file_name))

            for submission in problem.submissions:
                if submission.id == submission_id:
                    break
            else:
                continue

            if submission.author.email is None:
                continue

            language_name = get_file_extension(submission_file_name) + '/'
            new_submission_file_path = os.path.join(problem_path, language_name)

            if not os.path.isdir(new_submission_file_path):
                os.mkdir(os.path.join(problem_path, language_name))

            old_name = f'features/moodle_grades/submissions_temp/extracted_files/{submission_file_name}'
            new_name = os.path.join(new_submission_file_path, submission.author.email)

            if os.path.exists(new_name):
                os.remove(new_name)

            os.rename(
                str(old_name),
                str(new_name)
            )


def create_problem_folders(contest: Contest):
    parent_dir = f'features/moodle_grades/submissions_temp/{contest.id}'
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    for problem in contest.problems:
        path = os.path.join(parent_dir, f'{problem.name} {problem.index}')
        if not os.path.exists(path):
            os.mkdir(path)


def create_result_zip_file(contest_id: int) -> ZipFile:
    with ZipFile(f'features/moodle_grades/submissions_temp/{contest_id}.zip', 'w', ZIP_DEFLATED) as zip_ref:
        for dirname, _, files in os.walk(f'features/moodle_grades/submissions_temp/{contest_id}'):
            for file_name in files:
                zip_ref.write(
                    os.path.join(dirname, file_name),
                    os.path.relpath(
                        path=os.path.join(dirname, file_name),
                        start=f'features/moodle_grades/submissions_temp/{contest_id}'
                    )
                )

    return zip_ref


def get_file_name_without_extension(file_name: str):
    return ''.join(file_name.split('.')[:-1])


def get_file_extension(file_name: str):
    return file_name.split('.')[-1]


def calculate_points(
        results_data: MoodleResultsData,
        submission: Submission
) -> float:
    legal_excuse = results_data.legal_excuses.get(submission.author.email)
    deadline_offset = get_deadline_offset(legal_excuse, results_data.contest)
    deadline = results_data.contest.end_time_utc + deadline_offset

    points = apply_late_submission_policy(
        submission,
        deadline,
        results_data.late_submission_policy,
    )

    return points


def apply_late_submission_policy(
        submission: Submission,
        deadline: datetime,
        late_submission_policy: LateSubmissionPolicy
) -> float:
    extra_time = timedelta(seconds=late_submission_policy.extra_time)
    penalty = late_submission_policy.penalty

    submission_time_utc = submission.submission_time_utc
    late_submission_deadline = deadline + extra_time

    if submission_time_utc > late_submission_deadline:
        return 0.0

    if submission_time_utc > deadline:
        return submission.points * (1 - penalty)

    return submission.points


def get_deadline_offset(legal_excuse: LegalExcuse | None, contest: TimedEvent) -> timedelta:
    if legal_excuse is not None and legal_excuse.intersects_with(contest):
        return legal_excuse.end_time_utc - max(contest.start_time_utc, legal_excuse.start_time_utc)

    return timedelta(0)
