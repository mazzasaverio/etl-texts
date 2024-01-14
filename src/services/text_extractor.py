import os
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json
from loguru import logger
from dotenv import load_dotenv
import sys

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    "logs/esg_spider_{time}.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Load environment variables
load_dotenv()
source_path = os.getenv("PATH_SOURCE_TEXT_EXTRACTION")
destination_path = os.getenv("PATH_DESTINATION_TEXT_EXTRACTION")


def extract_text(file_path, file_path_output=None):
    try:
        elements = partition(filename=file_path, strategy="fast")
        logger.info(f"Extracted {len(elements)} elements")

        if file_path_output is not None:
            elements_to_json(elements, filename=file_path_output)
        return elements or []
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return []  # Return an empty list in case of an error


def file_already_processed(file_name, dest_path):
    """Check if a processed version of the file already exists, ignoring the extension."""
    file_root = os.path.splitext(file_name)[0]
    dest_files = [os.path.splitext(f)[0] for f in os.listdir(dest_path)]
    return file_root in dest_files


def get_list_files(source_path, destination_path):
    # Create a set of the root names of files in the destination directory for faster lookup
    dest_files = set(os.path.splitext(f)[0] for f in os.listdir(destination_path))

    logger.info(f"Found {len(dest_files)} documents in destination folder.")

    # Use list comprehension to filter and collect the files
    list_tot_files = [
        file
        for file in os.listdir(source_path)
        if file.endswith(".pdf") and os.path.splitext(file)[0] not in dest_files
    ]

    logger.info(
        f"Found {len(list_tot_files)} documents in source folder not yet processed."
    )

    return list_tot_files


def main():
    list_files = get_list_files(source_path, destination_path)
    len_source = len(list_files)
    len_destination = len(os.listdir(destination_path))
    logger.info(f"N. files source: {len_source} - N. files dest: {len_destination}")
    for filename in list_files:
        if filename.endswith(".pdf") and not file_already_processed(
            filename, destination_path
        ):
            logger.info(f"Processing file {filename}")
            file_path = os.path.join(source_path, filename)
            file_path_output = os.path.join(destination_path, filename)
            extract_text(file_path, file_path_output)

            len_source = len(list_files)
            len_destination = len(os.listdir(destination_path))
            logger.info(
                f"N. files source: {len_source} - N. files dest: {len_destination}"
            )
        else:
            logger.info(f"File {filename} already processed. Skipping.")


if __name__ == "__main__":
    main()
