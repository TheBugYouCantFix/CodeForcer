from domain.enums import Verdict
from domain.student import Student
from domain.contest import Contest, Problem, Submission
from datetime import datetime, timedelta
from unittest import mock

def test_map_handles_to_emails():

    # Mock handle to email mapper
    handle_to_email_mapper = mock.Mock()
    handle_to_email_mapper.side_effect = lambda handle: f"{handle}@example.com"

    # Create students
    student1 = Student(handle="student1", email=None)
    student2 = Student(handle="student2", email=None)
    student3 = Student(handle="student3", email="student3@example.com")

    # Create submissions
    submission1 = Submission(id=1, author=student1, verdict=Verdict.OK, passed_test_count=10, points=100.0,
                             programming_language="Python")
    submission2 = Submission(id=2, author=student2, verdict=Verdict.WRONG_ANSWER, passed_test_count=8, points=80.0,
                             programming_language="Java")
    submission3 = Submission(id=3, author=student3, verdict=Verdict.OK, passed_test_count=5, points=50.0,
                             programming_language="C++")

    # Create problems
    problem1 = Problem(index="A", name="Problem A", max_points=100.0, submissions=[submission1, submission3])
    problem2 = Problem(index="B", name="Problem B", max_points=100.0, submissions=[submission2])

    # Create contest
    contest = Contest(id=1, name="Contest 1", start_time=datetime.now(), duration=timedelta(hours=2),
                      problems=[problem1, problem2])

    # Call the method under test
    contest.map_handles_to_emails(handle_to_email_mapper)

    # Assertions
    assert student1.email == "student1@example.com"
    assert student2.email == "student2@example.com"
    assert student3.email == "student3@example.com"