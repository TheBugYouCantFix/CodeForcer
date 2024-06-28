from enum import Enum


class CfContestType(Enum):
    CF = 0
    IOI = 1
    ICPC = 2


class CfPhase(Enum):
    BEFORE = 0
    CODING = 1
    PENDING_SYSTEM_TEST = 2
    SYSTEM_TEST = 3
    FINISHED = 4


class CfProblemType(Enum):
    PROGRAMMING = 0
    QUESTION = 1


class CfParticipantType(Enum):
    CONTESTANT = 0
    PRACTICE = 1
    VIRTUAL = 2
    MANAGER = 3
    OUT_OF_COMPETITION = 4


class CfVerdict(Enum):
    FAILED = 0
    OK = 1
    PARTIAL = 2
    COMPILATION_ERROR = 3
    RUNTIME_ERROR = 4
    WRONG_ANSWER = 5
    PRESENTATION_ERROR = 6
    TIME_LIMIT_EXCEEDED = 7
    MEMORY_LIMIT_EXCEEDED = 8
    IDLENESS_LIMIT_EXCEEDED = 9
    SECURITY_VIOLATED = 10
    CRASHED = 11
    INPUT_PREPARATION_CRASHED = 12
    CHALLENGED = 13
    SKIPPED = 14
    TESTING = 15
    REJECTED = 16


class CfTestset:
    SAMPLES = 0
    PRETESTS = 1
    TESTS = 2
    CHALLENGES = 3
    TESTS1 = 4
    TESTS2 = 5
    TESTS3 = 6
    TESTS4 = 7
    TESTS5 = 8
    TESTS6 = 9
    TESTS7 = 10
    TESTS8 = 11
    TESTS9 = 12
    TESTS10 = 13
