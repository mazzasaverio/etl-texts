import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

# Local imports
from services.text_extractor import extract_text
from config.db_config import Config
from config.logger_config import logger
from database.models.docs_name_categ import DocsNameCateg

# Load environment variables
load_dotenv()

# Get source and destination paths from environment variables
path_source = os.getenv("PATH_SOURCE_DOCS")
path_destination = os.getenv("PATH_DESTINATION_TEXT_EXTRACTED")

# Validate source path
if not path_source:
    raise ValueError("Source path not set in .env file")

# Initialize FastAPI app
app = FastAPI()


def list_files(path, path_destination=None):
    """List all PDF files in the specified path."""
    return [
        doc
        for doc in os.listdir(path)
        if doc not in os.listdir(path_destination) and doc.endswith(".pdf")
    ]


@app.get("/")
def process_documents():
    """Process all PDF documents in the specified source path."""
    # List all PDF files in the source directory

    list_docs = list_files(path_source, path_destination)
    logger.info(f"Found {len(list_docs)} documents in source folder.")

    # Determine the number of CPU cores for parallel processing
    cpu_count = 2
    logger.info(f"Starting processing with {cpu_count} processes.\n\n")

    # Process documents in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        executor.map(handle_document, list_docs)


def handle_document(filename):
    """Handle the processing of a single document."""
    pid = multiprocessing.current_process().pid
    logger.info(f"\n\nProcessing file {filename} with process ID: {pid}")

    file_path = os.path.join(path_source, filename)
    file_name_without_extension, _ = os.path.splitext(filename)
    file_path_output = (
        os.path.join(path_destination, f"{file_name_without_extension}.json")
        if path_destination
        else None
    )

    len_source = len(os.listdir(path_source))
    len_destination = len(os.listdir(path_destination))
    logger.info(f"N. files source: {len_source} - N. files dest: {len_destination}")

    if path_destination and os.path.exists(file_path_output):
        logger.info(f"File {filename} already exists in destination. Skipping.")
        return

    if Config.MONGODB_URL:
        client = MongoClient(Config.MONGODB_URL)
        db = client.get_default_database()
        existing_doc = db.docs.find_one({"id_file": file_name_without_extension})

        if existing_doc:
            logger.info(f"Document {filename} already exists in database. Skipping.")
            return

    elements = extract_text(file_path, file_path_output)

    if Config.MONGODB_URL:
        doc = DocsNameCateg(
            id_file=file_name_without_extension,
            file_name=filename,
            date_download=datetime.now(),
            date_extraction=datetime.now(),
            elements=elements,
        )
        db.docs.insert_one(doc.model_dump())


if __name__ == "__main__":
    process_documents()
