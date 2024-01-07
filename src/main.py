from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from services.text_extractor import extract_text
from database.connection.odm_connection import Database
from database.models.docs_name_categ import DocsNameCateg
from datetime import datetime
from config.db_config import Config
from config.logger_config import logger

load_dotenv()

path_source = os.getenv("PATH_SOURCE_DOCS")
path_destination = os.getenv("PATH_DESTINATION_TEXT_EXTRACTED")

if not path_source:
    raise ValueError("Source path not set in .env file")


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database and other resources before startup
    await Database.initialize_database()
    yield
    # Clean up resources, if needed, before shutdown


app.lifespan = lifespan


@app.get("/")
async def process_documents():
    list_docs = os.listdir(path_source)
    logger.info(f"Found {len(list_docs)} documents in source folder.")
    for filename in list_docs:
        if filename.endswith(".pdf"):
            file_path = os.path.join(path_source, filename)
            file_name_without_extension, _ = os.path.splitext(filename)

            if path_destination:
                file_path_output = os.path.join(
                    path_destination, f"{file_name_without_extension}.json"
                )

                if os.path.exists(file_path_output):
                    logger.info(
                        f"File {filename} already exists in destination. Skipping."
                    )
                    continue
            else:
                file_path_output = None

            if Config.MONGODB_URL:
                existing_doc = await Database.get(file_name_without_extension)
                if existing_doc:
                    logger.info(
                        f"Document {filename} already exists in database. Skipping."
                    )
                    continue

            logger.info(f"Processing file: {filename}")
            elements = extract_text(file_path, file_path_output)

            if Config.MONGODB_URL:
                doc = DocsNameCateg(
                    id_file=file_name_without_extension,
                    file_name=filename,
                    date_download=datetime.now(),
                    date_extraction=datetime.now(),
                    elements=elements,
                )
                await Database.save(doc)


async def main():
    # await Database.initialize_database()
    await process_documents()


if __name__ == "__main__":
    # import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=8080)

    import asyncio

    asyncio.run(main())
