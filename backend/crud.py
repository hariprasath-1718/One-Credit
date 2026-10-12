from sqlalchemy.orm import Session

try:
    from backend import models, schemas
except ImportError:
    import models
    import schemas


def get_all_students(db: Session):
    """Retrieve all students from the database."""
    return db.query(models.Student).all()


def get_student_by_id(db: Session, student_id: int):
    """Retrieve a single student by their unique ID."""
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    """Retrieve a single student by their email address (used for duplicate checking)."""
    return db.query(models.Student).filter(models.Student.email == email).first()


def create_student(db: Session, student: schemas.StudentCreate):
    """Create and save a new student record in the database."""
    new_student = models.Student(
        name=student.name,
        age=student.age,
        department=student.department,
        email=student.email,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def update_student(
    db: Session, db_student: models.Student, student_update: schemas.StudentUpdate
):
    """Update an existing student's details in the database."""
    db_student.name = student_update.name
    db_student.age = student_update.age
    db_student.department = student_update.department
    db_student.email = student_update.email

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, db_student: models.Student):
    """Delete a student record from the database."""
    db.delete(db_student)
    db.commit()
    return db_student
