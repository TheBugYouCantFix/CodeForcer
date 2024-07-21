from typing import Annotated

from pydantic.functional_validators import AfterValidator

from src.features.contests.models import Submission, SubmissionSelector


def submission_name_validator(name: str) -> str:
    assert name in submission_selectors, "Invalid submission selector name"
    return name


SubmissionSelectorName = Annotated[str, AfterValidator(submission_name_validator)]

submission_selectors: dict[str, tuple[SubmissionSelector, str]] = {}


def submission_selector(name: str, description: str = ""):
    def decorator(selector: SubmissionSelector):
        submission_selectors[name] = selector, description
        return selector

    return decorator


@submission_selector("absolute best",
                     "selects the best submission, takes late submission policy and legal excuses into account")
def absolute_best_submission_selector(submissions: list[Submission]) -> Submission:
    return most_points_selector(submissions)


@submission_selector("latest", "selects the latest submission")
def latest_submission_selector(submissions: list[Submission]) -> Submission:
    return max(submissions, key=lambda s: s.submission_time_utc)


@submission_selector("latest successful", "returns latest unsuccessful submission if no successful submissions")
def latest_successful_submission_selector(submissions: list[Submission]) -> Submission:
    return max(submissions, key=lambda s: (s.is_successful, s.submission_time_utc))


@submission_selector("most points", "selects the submission with the most points on CodeForces")
def most_points_selector(submissions: list[Submission]) -> Submission:
    return max(
        submissions,
        key=lambda submission: (submission.points if submission.points is not None else 0,
                                submission.submission_time_utc)
    )


__all__ = ["submission_selectors", "SubmissionSelectorName", "submission_selector"]
