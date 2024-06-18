from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    email: EmailStr
    handle: str
