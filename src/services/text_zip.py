import os
import shutil
import zipfile
from dotenv import load_dotenv
from loguru import logger
import sys

# Load environment variables
load_dotenv()

# Setting up logging
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

# Retrieve paths from environment variables
PATH_SOURCE_FOR_ZIP = os.getenv("PATH_SOURCE_FOR_ZIP")
PATH_CHECK_FOLDER = os.getenv("PATH_CHECK_FOLDER")
PATH_DESTINATION_ZIP = os.getenv("PATH_DESTINATION_ZIP")
PATH_MOVE_DELETE_FOLDER = os.getenv("PATH_MOVE_DELETE_FOLDER")
NAME_ZIP_FILE = os.getenv("NAME_ZIP_FILE")


def get_filenames_without_extension(directory):
    """Returns a set of filenames without extensions in the given directory."""
    return {
        os.path.splitext(file)[0]
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    }


def zip_files(source_dir, dest_dir, check_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    source_files = get_filenames_without_extension(source_dir)
    logger.info(list(source_files)[:10])
    logger.info("----")
    check_files = get_filenames_without_extension(check_dir)
    logger.info(list(check_files)[:10])

    # Files present in both source and check directories
    files_to_zip = source_files.intersection(check_files)

    logger.info(f"{len(files_to_zip)} files to zip")

    zip_filename = os.path.join(dest_dir, NAME_ZIP_FILE)
    zipped_files = []

    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file in os.listdir(source_dir):
            file_name_without_extension = os.path.splitext(file)[0]
            if file_name_without_extension in files_to_zip and file.endswith("pdf"):
                file_path = os.path.join(source_dir, file)
                zipf.write(file_path, file)
                zipped_files.append(file)

    if zipped_files:
        logger.info(f"Files zipped successfully into {zip_filename}")
        move_pdf_files(source_dir, zipped_files)
    else:
        logger.warning("No files were zipped.")


def move_pdf_files(source_dir, zipped_files):
    if not os.path.exists(PATH_MOVE_DELETE_FOLDER):
        os.makedirs(PATH_MOVE_DELETE_FOLDER)

    for file in zipped_files:
        shutil.move(
            os.path.join(source_dir, file),
            os.path.join(PATH_MOVE_DELETE_FOLDER, file),
        )
        logger.info(f"Moved {file} to {PATH_MOVE_DELETE_FOLDER}")


def main():
    zip_files(PATH_SOURCE_FOR_ZIP, PATH_DESTINATION_ZIP, PATH_CHECK_FOLDER)


if __name__ == "__main__":
    main()
