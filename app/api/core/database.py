import asyncpg

from app.api.core.config import settings


async def get_db():
    return await asyncpg.create_pool(dsn=settings.database_url)