from dataclasses import dataclass


@dataclass
class Verdict:
    OK = 'OK'
    WRONG_ANSWER = 'WRONG_ANSWER'
    TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED'

