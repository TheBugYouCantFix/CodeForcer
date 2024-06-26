from application.students.students_service import StudentsService
from infrastructure.storage.db_students_repository import DBStudentsRepository


students_repository = DBStudentsRepository('students.db')
students_service = StudentsService(students_repository)
