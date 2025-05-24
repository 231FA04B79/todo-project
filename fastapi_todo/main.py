from fastapi import FastAPI, HTTPException, Request, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from fastapi.responses import JSONResponse
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from database import Base, engine, get_db  # 🔗 import from database.py

app = FastAPI()

# SQLAlchemy Student model
class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class Student(BaseModel):
    name: str
    age: int
    grade: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

class StudentOut(Student):
    id: int
    class Config:
        orm_mode = True

# Custom Exception
class StudentNotFound(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id

@app.exception_handler(StudentNotFound)
def student_not_found_handler(request: Request, exc: StudentNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with ID {exc.student_id} not found."},
    )

# POST - Create a new student
@app.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: Student, db: Session = Depends(get_db)):
    db_student = StudentModel(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# GET - Retrieve all students
@app.get("/students", response_model=List[StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()

# GET - Retrieve a single student by ID
@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise StudentNotFound(student_id)
    return db_student

# PUT - Fully update a student
@app.put("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise StudentNotFound(student_id)

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

# PATCH - Partially update a student
@app.patch("/students/{student_id}", response_model=StudentOut)
def partial_update_student(student_id: int, student: UpdateStudent, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise StudentNotFound(student_id)

    for key, value in student.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE - Delete a student
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise StudentNotFound(student_id)

    db.delete(db_student)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Student deleted successfully."})

# OPTIONS - Describe allowed methods for /students
@app.options("/students")
def options_students():
    return JSONResponse(
        status_code=200,
        headers={"Allow": "GET, POST, OPTIONS"},
        content={"message": "Allowed methods: GET, POST, OPTIONS"}
    )

# OPTIONS - Describe allowed methods for /students/{student_id}
@app.options("/students/{student_id}")
def options_student_by_id(student_id: int):
    return JSONResponse(
        status_code=200,
        headers={"Allow": "GET, PUT, PATCH, DELETE, OPTIONS"},
        content={"message": "Allowed methods: GET, PUT, PATCH, DELETE, OPTIONS"}
    )
