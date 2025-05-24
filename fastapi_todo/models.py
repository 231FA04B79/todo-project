# models.py
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy ORM model
class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)

# Pydantic schema for creating a student
class Student(BaseModel):
    name: str
    age: int
    grade: str

# Pydantic schema for partial update
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

# Pydantic schema for returning a student with ID
class StudentOut(Student):
    id: int

    class Config:
        orm_mode = True
