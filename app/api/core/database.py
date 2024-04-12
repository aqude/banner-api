import asyncpg

from api.core.config import settings


async def get_db():
    return await asyncpg.create_pool(dsn=settings.database_url)