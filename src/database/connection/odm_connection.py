# src/database/connection/odm_connection.py
from config.db_config import Config
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from database.models.docs_name_categ import DocsNameCateg
from config.logger_config import logger
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    client = None
    database_name = os.getenv("MONGODB_DATABASE")

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
