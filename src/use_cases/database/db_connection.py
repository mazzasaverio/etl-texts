from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class PdfDownload(Base):
    __tablename__ = "new_pdf_downloads"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    status = Column(String)  # 'success', 'failed', etc.
    notes = Column(String)  # Additional information like error messages
    download_path = Column(String)
    downloaded_at = Column(DateTime)
    keywords_namefile = Column(String)  # Column for keywords

    def __repr__(self):
        return f"<PdfDownload(url='{self.url}', status='{self.status}', downloaded_at='{self.downloaded_at}', keywords_namefile='{self.keywords_namefile}')>"


# Database credentials
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the connection string
connection_string = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

# Create engine and session
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)
