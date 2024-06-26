from pydantic import BaseModel
from results_scrapping_fields.enums_for_contest import *


class Contest(BaseModel):
    id: int
    name: str
    type: ContestType
    phase: Phase
    frozen: bool
    durationSeconds: int
    relativeTimeSeconds: int
    preparedBy: str | None = None
    websiteUrl: str | None = None
    description: str | None = None
    difficulty: int | None = None
    kind: str | None = None
    icpcRegion: str | None = None
    country: str | None = None
    city: str | None = None
    season: str | None = None

    class Config:
        arbitrary_types_allowed = True


class Problem(BaseModel):
    contestId: int | None = None
    problemsetName: str | None = None
    index: str
    name: str
    type: ProblemType
    points: float | None = None
    rating: int | None = None
    tags: list[str]


class Member(BaseModel):
    handle: str
    name: str | None = None


class Party(BaseModel):
    contestId: int | None = None
    members: [Member]
    participantType: ParticipantType
    teamId: int | None = None
    teamName: str | None = None
    ghost: bool
    room: int | None = None
    startTimeSeconds: int | None = None

    class Config:
        arbitrary_types_allowed = True


class RankListRow(BaseModel):
    party: Party
    rank: int
    points: float
    penalty: int
    successfulHackCount: int
    unsuccessfulHackCount: int
    problemResults: list[int]
    lastSubmissionTimeSeconds: int

    class Config:
        arbitrary_types_allowed = True
