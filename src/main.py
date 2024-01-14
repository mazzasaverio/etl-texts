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


# Setting up logger (assuming a similar setup as in settings.py)
def setup_logger():
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


setup_logger()


def main():
    logger.info("Starting ETL-Texts Pipeline")

    # Step 1: Text Extraction
    logger.info("Starting Text Extraction")
    extract_texts()
    logger.info("Text Extraction Completed")

    # Step 2: Text Translation
    logger.info("Starting Text Translation")
    translate_texts()
    logger.info("Text Translation Completed")

    # Step 3: Text Cleaning
    logger.info("Starting Text Cleaning")
    clean_texts()
    logger.info("Text Cleaning Completed")

    # Step 4: Text Embedding
    # Uncomment and adjust the following lines when text_embeddings service is ready
    # logger.info("Starting Text Embedding")
    # embed_texts()
    # logger.info("Text Embedding Completed")

    logger.info("ETL-Texts Pipeline Completed")


if __name__ == "__main__":
    main()
