import yaml
import os
import glob
from datetime import datetime

from text_extraction import extract_text
from text_process import process_json_elements
from database.session import session_scope
from database.models import TextData
from loguru import logger
import sys

from config.logger_config import logger


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def get_file_paths(folder_path):
    # Assuming the documents are PDFs, modify if different
    return glob.glob(os.path.join(folder_path, "*.pdf"))


def main():
    # Load configuration
    config = load_config()

    # Get path to the document folder
    document_folder = config["document_folder"]

    # Get list of file paths
    file_paths = get_file_paths(document_folder)

    # Process each file
    for file_path in file_paths:
        logger.info(f"Processing file: {file_path}")
        try:
            with session_scope() as session:
                # Check if file already processed
                exists = (
                    session.query(TextData)
                    .filter(TextData.file_name == file_path)
                    .first()
                )
                if not exists:
                    filename_output = extract_text(file_path)

                    logger.info(f"Extracted text to: {filename_output}")

                    # Define the element type and page range here
                    # element_types_list = ["NarrativeText"]
                    element_types_list = ["All"]
                    page_range = (1, 4)  # Example page range (inclusive)

                    # Process the JSON file
                    processed_text = process_json_elements(
                        filename_output, page_range, element_types_list
                    )

                    # Create new TextData object
                    element_types_string = ",".join(element_types_list)
                    new_record = TextData(
                        file_name=file_path.split("/")[-1],
                        processing_time=datetime.utcnow(),
                        extracted_pages=str(page_range),
                        element_types=element_types_string,
                        extracted_text=processed_text,
                    )
                    session.add(new_record)
                    logger.info(f"Processed and added: {file_path}")
                else:
                    logger.info(f"File already processed: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    main()
