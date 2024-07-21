import os
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

from fastapi import APIRouter, status, UploadFile, File, Form
from fastapi.responses import FileResponse

from src.features.contests.models import Contest

router = APIRouter()


@router.post('/submissions_archive', status_code=status.HTTP_200_OK)
async def sort_submissions_archive(
        contest: str = Form(...),
        submissions_archive: UploadFile = File(...)
) -> FileResponse:
    contest = Contest.model_validate_json(contest)

    await handle_sort_submissions_archive(contest, submissions_archive)
    os.rename(
        f'features/moodle_grades/submissions_temp/{contest.id}.zip',
        f'features/moodle_grades/submissions_temp/{contest.name}.zip'
    )

    return FileResponse(f'features/moodle_grades/submissions_temp/{contest.name}.zip', filename=f'{contest.name}.zip')


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
