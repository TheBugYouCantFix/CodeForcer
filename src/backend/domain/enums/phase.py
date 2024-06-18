from enum import Enum


class Phase(Enum):
    BEFORE = 0
    CODING = 1
    PENDING_SYSTEM_TEST = 2
    SYSTEM_TEST = 3
    FINISHED = 4
