from dataclasses import dataclass
from typing import List


@dataclass
class MoodleResultsData:
    contest: 'ContestData'
    plagiarizers: List[str]
    legally_excused: List[str]
    late_submission_rules: 'LateSubmissionRulesData'


@dataclass
class ContestData:
    id: int
    name: str
    problems: List['ProblemData']


@dataclass
class ProblemData:
    name: str
    index: str
    points: int
    max_points: int
    max_grade: int


@dataclass
class LateSubmissionRulesData:
    pass
