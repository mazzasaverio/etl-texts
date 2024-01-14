import os
import json
from dotenv import load_dotenv
from loguru import logger

from .utils.clean_text import (
    clean_text_type1,
)  # Assuming you have a text cleaning function

# Load environment variables
load_dotenv()
source_path = os.getenv("PATH_SOURCE_TEXT_CLEANING")
destination_path = os.getenv("PATH_DESTINATION_TEXT_CLEANING")


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def process_file(file_path):
    data = read_json(file_path)
    tot_text = " ".join([element["text_translated"] for element in data])
    logger.info(f"Cleaning text: {tot_text}")
    tot_text_cleaned = clean_text_type1(tot_text)

    return {
        "element_id": data[0]["element_id"],
        "filename": data[0]["filename"],
        "tot_text": tot_text,
        "tot_text_cleaned": tot_text_cleaned,
    }


def file_exists_in_destination(filename, dest_path):
    return os.path.exists(os.path.join(dest_path, filename))


def main():
    for filename in os.listdir(source_path):
        if filename.endswith(".json") and not file_exists_in_destination(
            filename, destination_path
        ):
            processed_data = process_file(os.path.join(source_path, filename))
            write_json(processed_data, os.path.join(destination_path, filename))


if __name__ == "__main__":
    main()
