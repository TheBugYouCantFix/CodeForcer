import pytest

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository
from tests.contests_test.data_generation import fake
from tests.mocks.contests_provider_mock import ContestsProviderMock
from tests.mocks.students_repository_mock import StudentRepositoryMock


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
def handle():
    return fake.word()
