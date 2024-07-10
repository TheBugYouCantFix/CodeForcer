from src.features.contests.provider import IContestsProvider
from src.features.contests.service import ContestsService
from src.features.students.repository import IStudentsRepository
from src.features.students.service import StudentsService
from src.features.moodle_grades.file_creator import MoodleGradesFileCreator
from src.features.contests.code_forces.request_sender import CodeForcesRequestsSender
from src.features.students.storage.db_repository import DBStudentsRepository
from src.features.contests.code_forces.contests_provider import CodeForcesContestsProvider
from src.utils.dependencies_container import DependenciesContainer

container = DependenciesContainer()

container[IContestsProvider] = lambda: CodeForcesContestsProvider(
    requests_sender_factory=CodeForcesRequestsSender,
    anonymous_requests_sender_factory=CodeForcesRequestsSender
)
container[IStudentsRepository] = lambda: DBStudentsRepository('students.db')

container[StudentsService] = lambda: StudentsService(container[IStudentsRepository], container[IContestsProvider])
container[ContestsService] = lambda: ContestsService(container[IContestsProvider], container[IStudentsRepository])
container[MoodleGradesFileCreator] = MoodleGradesFileCreator
