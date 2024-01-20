import os
import json
from loguru import logger
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.services.utils.clean_text import clean_text_type1


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def process_file(file_path):
    data = read_json(file_path)
    try:
        tot_text = " ".join([element["text_translated"] for element in data])
        tot_text_cleaned = clean_text_type1(tot_text)

        return {
            "filename": data[0]["filename"],
            "tot_text_cleaned": tot_text_cleaned,
            "tot_text_raw": tot_text,
        }
    except Exception as e:
        logger.error(f"Error cleaning text from {file_path}: {e}")
        return {}


def file_exists_in_destination(filename, dest_path):
    return os.path.exists(os.path.join(dest_path, filename))


def main(source_path, destination_path):
    for filename in os.listdir(source_path):
        if filename.endswith(".json") and not file_exists_in_destination(
            filename, destination_path
        ):
            processed_data = process_file(os.path.join(source_path, filename))
            if processed_data:
                write_json(processed_data, os.path.join(destination_path, filename))


if __name__ == "__main__":
    main(source_path, destination_path)
