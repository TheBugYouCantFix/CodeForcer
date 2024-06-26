from application.students.students_service import StudentsService
from infrastructure.storage.db_students_repository import DBStudentsRepository


repository = DBStudentsRepository('students.db')
service = StudentsService(repository)
