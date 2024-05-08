import logging

from tortoise import Tortoise

from app.settings.config import settings


async def startup_db():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules=settings.MODELS
    )

    await Tortoise.generate_schemas()
    logging.info("Database setup complete")


async def shutdown_db():
    await Tortoise.close_connections()
    logging.info("Database shutdown complete")
