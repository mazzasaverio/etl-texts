# Import necessary libraries
from datasets import Dataset, DatasetDict, load_dataset
import json
import os
from glob import glob

from dotenv import load_dotenv
from loguru import logger
import sys

# Load environment variables
load_dotenv()

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


def main():
    # Read the input and output paths from environment variables
    data_dir = os.getenv("PATH_SOURCE_TEXT_SAVE_FINAL_FORMAT", "/default/input/path")
    output_path = os.getenv(
        "PATH_DESTINATION_TEXT_SAVE_FINAL_FORMAT", "/default/output/path"
    )

    generation_date = "2024_01_19"

    # Load all JSON files in the specified directory
    json_files = glob(os.path.join(data_dir, "*.json"))

    def validate_and_fill_json_file(file_path, default_value="N/A"):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Function to process a single record (dictionary)
            def process_record(record):
                keys = list(record.keys())

                for key in keys:
                    # Replace None with default value
                    if record[key] is None:
                        record[key] = default_value
                    # Convert integers to strings
                    elif isinstance(record[key], int):
                        logger.info(f"{file_path}")
                        logger.info(f"Converting {key}: {record[key]} to string")
                        record[key] = str(record[key])

                    record["generation_date"] = generation_date

            # Check if the loaded data is a dictionary (single record)
            if isinstance(data, dict):
                process_record(data)
            # Check if the loaded data is a list (multiple records)
            elif isinstance(data, list):
                for record in data:
                    process_record(record)
            else:
                logger.error(
                    f"Invalid JSON structure in file {file_path}: Expected a dict or list, got {type(data).__name__}"
                )

            return data

    processed_data = []
    for json_file in json_files:
        processed_data.append(validate_and_fill_json_file(json_file))

    json_file_path = os.path.join(output_path, "campany_reports.json")

    # Save the dictionary as a JSON file
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(processed_data, file, indent=4)


if __name__ == "__main__":
    main()
