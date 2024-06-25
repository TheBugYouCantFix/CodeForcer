from pydantic import BaseModel


class Member(BaseModel):
    handle: str
    name: str | None = None


class Party(BaseModel):
    contestId: int
    members: [Member]

    class Config:
        arbitrary_types_allowed = True


class RankListRow(BaseModel):
    party: Party
    rank: int | None = None
    point: int
    penalty: int | None = None
    points: float | None = None
    problemResults: int | None = None

    class Config:
        arbitrary_types_allowed = True
