from pydantic import BaseModel


class Problem(BaseModel):
    index: str
    contest_id: int
    name: str
    max_points: int
