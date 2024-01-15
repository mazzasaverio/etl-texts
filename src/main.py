import os
from dotenv import load_dotenv
from loguru import logger
import sys

# Import the services
from services.text_extractor import main as extract_texts
from services.text_translator import process_files as translate_texts
from services.text_cleaner import main as clean_texts

# from services.text_embeddings import main as embed_texts  # Assuming similar structure for text_embeddings

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


def main():
    logger.info("Starting ETL-Texts Pipeline")

    # Step 1: Text Extraction
    logger.info("Starting Text Extraction")
    extract_texts()
    logger.info("Text Extraction Completed")

    # Step 2: Text Translation
    logger.info("Starting Text Translation")
    source_path = os.getenv("PATH_SOURCE_TEXT_TRANSLATION")
    destination_path = os.getenv("PATH_DESTINATION_TEXT_TRANSLATION")
    target_language = os.getenv("TARGET_LANGUAGE_TRANSLATION")

    translate_texts(source_path, destination_path, target_language)
    logger.info("Text Translation Completed")

    # Step 3: Text Cleaning
    logger.info("Starting Text Cleaning")
    clean_texts()
    logger.info("Text Cleaning Completed")

    logger.info("ETL-Texts Pipeline Completed")


if __name__ == "__main__":
    main()
