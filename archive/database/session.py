import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from contextlib import contextmanager

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the connection string
connection_string = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

# Create engine
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
