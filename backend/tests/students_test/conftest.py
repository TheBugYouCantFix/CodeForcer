import pytest
from faker import Faker

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository
from tests.contests_test.data_generation import fake
from tests.mocks.contests_provider_mock import ContestsProviderMock
from tests.mocks.students_repository_mock import StudentRepositoryMock


fake = Faker('en-US')


@pytest.fixture(autouse=True)
def setup_and_teardown(contests_provider_mock, students_repo_mock):
    yield
    contests_provider_mock.valid_handles = []
    students_repo_mock.db.clear()
    print('mocks cleared')


@pytest.fixture
def contests_provider_mock():
    contests_provider_mock = ContestsProviderMock()
    container[IContestsProvider] = contests_provider_mock
    return contests_provider_mock


@pytest.fixture
def students_repo_mock():
    students_repo_mock = StudentRepositoryMock()
    container[IStudentsRepository] = students_repo_mock
    return students_repo_mock


@pytest.fixture
def email():
    return fake.email()


@pytest.fixture
def invalid_email():
    return fake.email() + '!'


@pytest.fixture
def handle():
    return fake.word()
