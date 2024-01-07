# PDFs Text Extraction

## Overview

This repository provides a foundational framework for text extraction from a list of PDF files. It's designed to offer a starting point for projects that require efficient and automated text extraction from PDF documents.

## Configuration

Configuration settings are managed via a `.env` file. This includes:

- **Data Source**: Specifying the source of the PDF files.
- **Data Destination**: Defining the output destination, which can be another folder or a database.
- **Environment Setup**: Setting the operational mode (Development or Production) to ensure optimal performance and resource utilization.

## Key Features

- **FastAPI Integration**: Utilizes FastAPI for handling HTTP requests, allowing for scalable and efficient request management. This is particularly useful for handling various types of processing tasks in a web service context.
- **Benie as ODM**: Currently, Benie is used as the Object Document Mapper (ODM) primarily with MongoDB. Future updates will include support for other NoSQL databases, as well as SQL databases using SQLAlchemy ORM.
- **Text Extraction**: Leverages `unstructured` for automated text extraction with partitioning capabilities. This feature is crucial for handling large volumes of PDF files and extracting text efficiently.

## Future Enhancements

- **Parallel Processing**: The next step is to implement parallel processing for the text extractor. This enhancement aims to significantly improve the efficiency and speed of text extraction from multiple PDF files simultaneously.

## Getting Started

1. Clone the repository.
2. Configure your `.env` file with the appropriate settings.
3. Install required dependencies.
4. Run the application in your chosen environment (Development or Production).

## Contribution

Contributions to enhance this project are welcome. Feel free to fork the repository, make improvements, and submit a pull request.

## License

This project is open-sourced under the [MIT License](LICENSE).
