import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    """
    Shared Pydantic fields for creating and updating a student.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    age: int = Field(..., gt=0, le=120, description="Student's age (must be between 1 and 120)")
    department: str = Field(..., min_length=1, max_length=100, description="Student's department")
    email: str = Field(..., min_length=3, max_length=150, description="Student's email address")

    @field_validator("name", "department")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        """Ensure text fields are not just whitespace."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty or blank.")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        """Validate that the email has a standard format (e.g., user@example.com)."""
        cleaned = value.strip().lower()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(email_pattern, cleaned):
            raise ValueError("Invalid email address format.")
        return cleaned


class StudentCreate(StudentBase):
    """Schema used when creating a new student (POST /students)."""
    pass


class StudentUpdate(StudentBase):
    """Schema used when updating an existing student (PUT /students/{student_id})."""
    pass


class StudentResponse(StudentBase):
    """
    Schema used for returning student data in API responses.
    Includes the auto-generated database 'id'.
    """
    id: int

    # Allows Pydantic to read data directly from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)
