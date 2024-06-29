from pydantic import BaseModel, EmailStr


class ContestParticipant(BaseModel):
    handle: str


class Student(ContestParticipant):
    email: EmailStr
