from dataclasses import dataclass

from results_scrapping_fields.enums_for_contest import *


@dataclass
class Contest:
    id: int
    name: str
    type: ContestType
    phase: Phase
    frozen: bool
    durationSeconds: int
    startTimeSeconds: int
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


@dataclass
class Problem:
    index: str
    type: ProblemType
    name: str
    tags: list[str]
    contestId: int | None = None
    problemsetName: str | None = None
    points: float | None = None
    rating: int | None = None


@dataclass
class Member:
    handle: str
    name: str | None = None


@dataclass
class Party:
    members: [Member]
    ghost: bool
    participantType: ParticipantType
    teamId: int | None = None
    teamName: str | None = None
    room: int | None = None
    contestId: int | None = None
    startTimeSeconds: int | None = None


@dataclass
class RankListRow:
    party: Party
    rank: int
    points: float
    penalty: int
    successfulHackCount: int
    unsuccessfulHackCount: int
    problemResults: list[int]
    lastSubmissionTimeSeconds: int | None = None
