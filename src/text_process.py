import json
from utils.logger_config import logger


def process_json_elements(json_file_path, page_range, element_types=["All"]):
    logger.info(f"Processing JSON file: {json_file_path}")

    # Load JSON data from the file
    with open(json_file_path, "r") as file:
        elements = json.load(file)
        logger.info(f"Loaded {len(elements)} elements from the file.")

    # Filter elements based on type (if provided) and page number range
    if element_types[0] != "All":
        filtered_elements = [
            elem
            for elem in elements
            if elem["type"] in element_types
            and page_range[0] <= elem["metadata"]["page_number"] <= page_range[1]
        ]
        logger.info(
            f"Filtered elements by types {element_types} and page range {page_range}."
        )
    else:
        filtered_elements = [
            elem
            for elem in elements
            if page_range[0] <= elem["metadata"]["page_number"] <= page_range[1]
        ]
        logger.info(
            f"Filtered elements by page range {page_range} without type restriction."
        )

    logger.info(f"Number of elements after filtering: {len(filtered_elements)}")

    # Concatenate the text of the filtered elements
    concatenated_text = " ".join([elem["text"] for elem in filtered_elements])
    logger.info("Concatenated text from filtered elements.")

    return concatenated_text
