from enum import Enum


class ContestType(Enum):
    CF = 0
    IOI = 1
    ICPC = 2


class Phase(Enum):
    BEFORE = 0
    CODING = 1
    PENDING_SYSTEM_TEST = 2
    SYSTEM_TEST = 3
    FINISHED = 4


class ProblemType(Enum):
    PROGRAMMING = 0
    QUESTION = 1


class ParticipantType(Enum):
    CONTESTANT = 0
    PRACTICE = 1
    VIRTUAL = 2
    MANAGER = 3
    OUT_OF_COMPETITION = 4
