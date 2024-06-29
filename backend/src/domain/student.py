from __future__ import annotations

from pydantic import BaseModel, EmailStr


class ContestParticipant(BaseModel):
    handle: str


class Student(ContestParticipant):
    email: EmailStr

    def lower(self) -> Student:
        return Student(email=self.email, handle=self.handle.lower())


