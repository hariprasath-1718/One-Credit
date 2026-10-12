from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL (creates a file named 'students.db' in the project root directory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed only for SQLite to allow multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session for each API request
    and automatically closes it once the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
