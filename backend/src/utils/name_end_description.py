from pydantic import BaseModel


class NameAndDescription(BaseModel):
    name: str
    description: str
