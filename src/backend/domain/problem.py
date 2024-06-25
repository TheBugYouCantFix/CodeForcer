from pydantic import BaseModel


class Problem(BaseModel):
    contestId: int
    problemsetName: str | None = None
    index: str
    points: float | None = None
    rating: int | None = None
    tags: list[str]
