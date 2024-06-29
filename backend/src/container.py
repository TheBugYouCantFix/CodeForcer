from application.contests.contests_service import ContestsService
from application.students.students_service import StudentsService
from infrastructure.storage.db_students_repository import DBStudentsRepository
from infrastructure.code_forces.code_forces_contests_provider import CodeForcesContestsProvider
from application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator

students_repository = DBStudentsRepository('students.db')
students_service = StudentsService(students_repository)

contests_provider = CodeForcesContestsProvider()
contests_service = ContestsService(contests_provider, students_repository)
moodle_grades_file_creator = MoodleGradesFileCreator()
