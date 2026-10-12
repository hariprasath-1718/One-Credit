from sqlalchemy import Column, Integer, String

try:
    from backend.database import Base
except ImportError:
    from database import Base


class Student(Base):
    """
    SQLAlchemy ORM model representing the 'students' table in the SQLite database.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
