from application.contests.contests_service import ContestsService
from application.students.students_service import StudentsService
from infrastructure.code_forces.requests_sending.code_forces_request_sender import CodeForcesRequestsSender
from infrastructure.storage.db_students_repository import DBStudentsRepository
from infrastructure.code_forces.code_forces_contests_provider import CodeForcesContestsProvider
from application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator

students_repository = DBStudentsRepository('students.db')
contests_provider = CodeForcesContestsProvider(
    requests_sender_factory=lambda key, secret: CodeForcesRequestsSender(key, secret),
    anonymous_requests_sender_factory=lambda: CodeForcesRequestsSender()
)

students_service = StudentsService(students_repository, contests_provider)
contests_service = ContestsService(contests_provider, students_repository)
moodle_grades_file_creator = MoodleGradesFileCreator()
