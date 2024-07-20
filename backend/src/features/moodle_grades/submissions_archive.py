import zipfile, shutil, time, os

from io import BytesIO

from fastapi import APIRouter, status, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse

from src.features.contests.models import Contest, Problem, Submission
from src.features.contests.get_contest import GetContestQuery
from src.features.students.get_student import GetStudentQueryHandler
from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository

router = APIRouter()

@router.post('/submissions_archive', status_code=status.HTTP_200_OK)
async def sort_submissions_archive(api_key: str, api_secret: str, submissions_archive: UploadFile = File(...)) -> FileResponse:

    result_buffer = BytesIO()








    class SubmissionsArchiveSorterHandler:
        def handle(self, api_key: str, api_secret: str, submissions_archive: UploadFile = File(...)) -> BytesIO:
            archive_bytes = submissions_archive.read()

            with zipfile.ZipFile(BytesIO(archive_bytes), 'r') as zip_ref:
                zip_ref.extractall('features/moodle_grades/submissions_temp/extracted_files/')
                submissions_names = zip_ref.namelist()
                contest: Contest = self._get_contest(int(self._get_file_name_without_type(submissions_archive.filename)),
                                                     api_key, api_secret)
                self._create_result_folder(contest, submissions_names)

            result = self._create_result_zip_file()





        def _get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
            get_contest_query = GetContestQuery(IContestsProvider, IStudentsRepository)
            return get_contest_query.handle(contest_id, api_key, api_secret)

        def _get_file_name_without_type(self, file_name: str):
            return file_name.split('.')[0]

        def _get_file_type(self, file_name: str):
            return file_name.split('.')[1]

        def _create_result_folder(self, contest: Contest, submissions_names: list[str]):
            self._create_problem_folders(contest)
            self._fill_problem_folders(contest, submissions_names)

        def _create_problem_folders(self, contest: Contest):
            os.mkdir(f'features/moodle_grades/submissions_temp/{str(contest.id)}')
            parent_dir = f'features/moodle_grades/submissions_temp/{str(contest.id)}/'
            for problem in contest.problems:
                directory = f'{problem.name}'
                path = os.path.join(parent_dir, directory)
                os.makedir(path)

        def _fill_problem_folders(self, contest: Contest, submissions_names: list[str]):
            parent_dir = f'features/moodle_grades/submissions_temp/{str(contest.id)}'
            for problem in contest.problems:
                directory = f'{problem.name}/'
                problem_path = os.path.join(parent_dir, directory)
                for submission_name in submissions_names:
                    submission_id = int(self._get_file_name_without_type(submission_name))
                    if any(submission.id == submission_id for submission in problem.submissions):
                        if (os.path.isdir(os.path.join(problem_path, f'{self._get_file_type(submission_name)}'))):
                            shutil.move(f'feature/moodle_grades/submission_temp/extracted_files/{sibmission_name}',
                                        os.path.join(problem_path, f'{self._get_file_type(submission_name)}'))
                        else:
                            os.mkdir(os.path.join(problem_path, f'{self._get_file_type(submission_name)}/'))

                        language_folder = os.path.join(problem_path, f'{self._get_file_type(submission_name)}')

                        os.rename(os.path.join(language_folder, f'{submission_name}'),
                                  os.path.join(language_folder, f'{self._get_student_email(submission)}'))

        def _get_student_email(self, submission: Submission):
            get_student_query_handle = GetStudentQueryHandler(IStudentsRepository)
            return get_student_query_handle.handle(submission.author.handle).email

        def _create_result_zip_file(self, contest_id: str) -> zipfile.ZipFile:
            with zipfile.ZipFile(f'features/moodle_grades/submissions_temp/{contest_id}.zip',
                                 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for dirname, subdirs, files in os.walk(f'features/moodle_grades/submissions_temp/{contest_id}'):
                    zip_ref.write(dirname)
                    for file_name in files:
                        zip_ref.write(os.path.join(dirname, file_name))

            return zip_ref