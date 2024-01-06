from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
import os
from utils.logger_config import logger


def extract_text(filename):
    elements = partition_pdf(filename=filename)

    filename_output = (
        f"data/processed/{os.path.basename(filename).replace('.pdf', '.json')}"
    )

    elements_to_json(elements, filename=filename_output)

    return filename_output
