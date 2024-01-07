# src/database/connection/odm_connection.py
from config.db_config import Config
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from database.models.docs_name_categ import DocsNameCateg
import yaml
from config.logger_config import logger  # Make sure to import the logger
from pathlib import Path

# Correct the path by using pathlib
config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

with config_path.open() as config_file:
    config = yaml.safe_load(config_file)


class Database:
    client = None
    database_name = database_name = config["mongodb"]["database_name"]

    @classmethod
    async def initialize_database(cls):
        try:
            cls.client = AsyncIOMotorClient(Config.MONGODB_URL)
            await init_beanie(
                database=cls.client[cls.database_name], document_models=[DocsNameCateg]
            )

            # Initialize the collection by creating an index, this will create the collection if it doesn't exist.
            await DocsNameCateg.get_motor_collection().create_index(
                "id_file", unique=True
            )
            logger.info("Index on 'id_file' created.")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise e

    @classmethod
    async def save(cls, document):
        await document.insert()

    @classmethod
    async def get(cls, id):
        return await DocsNameCateg.get(id)

    @classmethod
    async def get_all(cls):
        return await DocsNameCateg.find_all().to_list()

    @classmethod
    async def delete(cls, id):
        doc = await cls.get(id)
        if doc:
            await doc.delete()
            return True
        return False
