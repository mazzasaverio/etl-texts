from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json
from config.logger_config import logger


def extract_text(file_path, file_path_output=None):
    try:
        elements = partition(filename=file_path, strategy="fast")

        logger.info(f"Extracted {len(elements)} elements")

        if file_path_output is not None:
            elements_to_json(elements, filename=file_path_output)
            return elements or []  # Return an empty list if elements is None
        else:
            return (
                elements_to_json(elements) or []
            )  # Return an empty list if elements is None
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return []  # Return an empty list in case of an error
