from pydantic import BaseModel
from enums.phase import Phase


class Contest(BaseModel):
    id: int
    phase: Phase
    problem_indices: [str]
