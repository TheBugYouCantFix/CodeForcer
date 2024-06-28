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
