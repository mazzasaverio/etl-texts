# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()

# Base = declarative_base()


# class NewPdfDownload(Base):
#     __tablename__ = "new_pdf_downloads"
#     id = Column(Integer, primary_key=True)
#     url = Column(String)
#     file_name = Column(String)
#     status = Column(String)
#     keywords_namefile = Column(String)
#     downloaded_at = Column(DateTime, default=datetime.utcnow)


# # Database credentials
# db_username = os.getenv("DB_USERNAME")
# db_password = os.getenv("DB_PASSWORD")
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")

# # Create the connection string
# connection_string = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

# # Create engine and session
# engine = create_engine(connection_string)
# Session = sessionmaker(bind=engine)


# def create_tables():
#     Base.metadata.create_all(engine)


from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class FileDownload(Base):
    __tablename__ = "downloads"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    file_name = Column(String)
    status = Column(String)
    downloaded_at = Column(DateTime, default=datetime.utcnow)


# Percorso del file del database SQLite
DATABASE_URL = "sqlite:////home/sam/github/google-crawler-data/data/database.db"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)
