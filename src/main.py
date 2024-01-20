import os
from dotenv import load_dotenv
from loguru import logger
import sys

# Import the services
from services.text_extractor import main as extract_texts
from services.text_translator import main as translate_texts
from services.text_cleaner import main as clean_texts

# Load environment variables
load_dotenv()

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    "logs/etl_texts_{time}.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


def get_path(env_var, use_test_data=False):
    base_path = os.getenv(env_var)
    if use_test_data:
        # Splitting the path and inserting 'test_data' before the last component
        path_parts = base_path.split(os.sep)
        path_parts.insert(-1, "test_data")
        return os.path.join(*path_parts)
    return base_path


def main(use_test_data=False):
    logger.info("Starting ETL-Texts Pipeline")

    # Step 1: Text Extraction
    logger.info("Starting Text Extraction")
    source_path = get_path("PATH_SOURCE_TEXT_EXTRACTION", use_test_data)
    destination_path = get_path("PATH_DESTINATION_TEXT_EXTRACTION", use_test_data)
    extract_texts(source_path, destination_path)
    logger.info("Text Extraction Completed")

    # Step 2: Text Translation
    logger.info("Starting Text Translation")
    source_path = get_path("PATH_SOURCE_TEXT_TRANSLATION", use_test_data)
    destination_path = get_path("PATH_DESTINATION_TEXT_TRANSLATION", use_test_data)
    target_language = os.getenv("TARGET_LANGUAGE_TRANSLATION")
    translate_texts(source_path, destination_path, target_language)
    logger.info("Text Translation Completed")

    # Step 3: Text Cleaning
    logger.info("Starting Text Cleaning")
    source_path = get_path("PATH_SOURCE_TEXT_CLEANING", use_test_data)
    destination_path = get_path("PATH_DESTINATION_TEXT_CLEANING", use_test_data)
    clean_texts(source_path, destination_path)
    logger.info("Text Cleaning Completed")

    logger.info("ETL-Texts Pipeline Completed")


if __name__ == "__main__":
    main(use_test_data=True)
