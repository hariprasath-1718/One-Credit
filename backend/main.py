from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

try:
    from backend import crud, models, schemas
    from backend.database import engine, get_db
except ImportError:
    import crud
    import models
    import schemas
    from database import engine, get_db

# Create the SQLite database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint to verify that the FastAPI server is running."""
    return {"message": "Welcome to the Student Management System API"}


@app.get("/students", response_model=List[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    """
    GET /students
    Retrieve and return all students from the database.
    """
    students = crud.get_all_students(db)
    return students


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    GET /students/{student_id}
    Retrieve a single student by their unique ID.
    """
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID. ID must be a positive integer.",
        )

    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )
    return db_student


@app.post(
    "/students",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    POST /students
    Create a new student record after checking for duplicate email addresses.
    """
    existing_student = crud.get_student_by_email(db, email=student.email)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered to another student.",
        )

    return crud.create_student(db=db, student=student)


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db),
):
    """
    PUT /students/{student_id}
    Update an existing student's details by ID.
    """
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID. ID must be a positive integer.",
        )

    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    # Check if the updated email conflicts with a different student's email
    existing_email_student = crud.get_student_by_email(db, email=student_update.email)
    if existing_email_student and existing_email_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered to another student.",
        )

    return crud.update_student(
        db=db, db_student=db_student, student_update=student_update
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    DELETE /students/{student_id}
    Delete an existing student by ID.
    """
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID. ID must be a positive integer.",
        )

    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    crud.delete_student(db=db, db_student=db_student)
    return {"message": f"Student with ID {student_id} deleted successfully."}
