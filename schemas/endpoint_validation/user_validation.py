from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    first_name: str
    last_name: str
    major: str
    year: int

