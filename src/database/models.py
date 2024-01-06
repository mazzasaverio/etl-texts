from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()


class TextData(Base):
    __tablename__ = "text_data"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True)
    processing_time = Column(DateTime, default=datetime.utcnow)
    extracted_pages = Column(String)
    element_types = Column(String)  # Storing element types as a string
    extracted_text = Column(String)

    def __repr__(self):
        return f"<TextData(file_name={self.file_name}, processing_time={self.processing_time})>"
