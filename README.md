# ETL-Texts

## Overview

ETL-Texts has the aim of becoming one pipeline designed for extracting, translating, cleaning, and transforming text files, making them readily usable for different objectives. It operates on the principle that each step in the process requires an input path and an output path, allowing for independent execution or a sequential flow through the pipeline.

## **Features**

### Services

The services in ETL-Texts are dedicated to primary text processing operations, including extraction, translation, and cleaning. Each service module can function independently or as part of an integrated pipeline.

- **Text Extraction**:

  - **File**: `src/services/text_extractor.py`
  - **Description**: This service uses the `unstructured` package to extract text from various document formats, effectively handling diverse types of unstructured data.

- **Text Translation**:

  - **File**: `src/services/text_translator.py`
  - **Description**: Leveraging a multilingual model, this service provides optional text translation, facilitating multilingual data processing and analysis.

- **Text Cleaning**:
  - **File**: `src/services/text_cleaner.py`
  - **Description**: Responsible for aggregating and cleaning text data according to specific requirements, this service ensures that the text is standardized and ready for further analysis. (Currently under development)

### Use Cases

Use case modules in ETL-Texts are focused on applying the processed text to specific tasks or analyses, utilizing advanced models and techniques.

- **Information Extraction**:
  - **File**: `src/use_cases/info_extraction.py`
  - **Description**: This module extracts specific information from texts using the GPT-3.5 model. It processes cleaned text files, sending parts of the text to the GPT-3.5 API and retrieving structured information as a response. This structured information is then saved in a JSON format at the designated output path, enriching the cleaned text with valuable insights extracted by GPT-3.5.

The system is built on the principle that a file will be processed only if it hasn't been processed previously, which is determined by checking the destination path. Outputs are consistently formatted in JSON to facilitate flexible manipulation and ingestion stages.

## Configuration

Input and output paths are set through the `.env` file (refer to `.env.example`, which should be renamed to `.env`).

## Roadmap

- Parallelization and containerization of the process for enhanced performance.
- Automation of the process by orchestrating an event-driven pipeline capable of leveraging serverless computing depending on the scale and processing time requirements.
- Provisioning for varied inputs and outputs to facilitate choice or alternation between data lakes, SQL databases, or NoSQL databases.
