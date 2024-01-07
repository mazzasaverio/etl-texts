from contextlib import asynccontextmanager
import os
import yaml
from fastapi import FastAPI
from services.text_extractor import extract_text
from database.connection.odm_connection import Database
from database.models.docs_name_categ import DocsNameCateg
from datetime import datetime
from config.logger_config import logger
from pathlib import Path

app = FastAPI()

# Load configurations
config_path = Path(__file__).parent / "config" / "config.yaml"
with config_path.open() as config_file:
    config = yaml.safe_load(config_file)

document_folder = config["document_folder"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database and other resources before startup
    await Database.initialize_database()
    yield
    # Clean up resources, if needed, before shutdown


app.lifespan = lifespan


@app.get("/")
async def process_documents():
    for filename in os.listdir(document_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(document_folder, filename)
            file_name_without_extension, _ = os.path.splitext(filename)
            file_path_output = f"data/processed/{filename.replace('.pdf', '.json')}"
            logger.info(f"Processing file: {filename}")
            elements = extract_text(file_path, file_path_output)

            # Create and save document instance in MongoDB
            doc = DocsNameCateg(
                id_file=file_name_without_extension,  # Set an appropriate id
                file_name=filename,
                date_download=datetime.now(),
                date_extraction=datetime.now(),
                elements=elements,
            )
            await Database.save(doc)


async def main():
    await Database.initialize_database()
    await process_documents()


if __name__ == "__main__":
    # import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=8080)

    import asyncio

    asyncio.run(main())
