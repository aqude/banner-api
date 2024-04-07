from app.api.core.database import get_db
from app.exceptions import NotFoundError
from app.schemas.banner import BannerCreate, BannerUpdate


async def get_banner_for_user(tag_id, feature_id, use_last_revision):
    async with (await get_db()).acquire() as conn:
        use_last_revision_query = """
        SELECT * FROM user_banners
            WHERE tag_id =? AND feature_id =?
            ORDER BY revision DESC
            LIMIT 1
        """
        else_query = """
        SELECT * FROM user_banners
            WHERE tag_id =? AND feature_id =?
        """
        if use_last_revision:
            query = use_last_revision_query
            values = (tag_id, feature_id)
        else:
            query = else_query
            values = (tag_id, feature_id)
        banner = await conn.fetchrow(query, *values)
        if banner:
            return banner
        else:
            return None


async def get_all_banners(feature_id, tag_id, limit, offset):
    async with (await get_db()).acquire() as conn:
        query = """
        SELECT * FROM user_banners
            WHERE feature_id =? AND tag_id =?
            LIMIT ? OFFSET ?
        """
        values = (feature_id, tag_id, limit, offset)
        banners = await conn.fetch(query, *values)
        return banners

async def create_banner(banner: BannerCreate):
    async with (await get_db()).acquire() as conn:
        query = """
        INSERT INTO user_banners
            (tag_ids, feature_id, title, text, url, is_active)
        VALUES
            (?, ?, ?, ?, ?, ?)
        """
        values = (
            banner.tag_ids,
            banner.feature_id,
            banner.content.title,
            banner.content.text,
            banner.content.url,
            banner.is_active
        )
        await conn.execute(query, *values)
        return banner.tag_id


async def update_banner(id, banner: BannerUpdate):
    async with (await get_db()).acquire() as conn:
        query = """
        UPDATE user_banners
            SET title = ?, text = ?, url = ?, is_active = ?
        WHERE id = ?
        """
        values = (id, banner.content.title, banner.content.text, banner.content.url, banner.is_active)
        await conn.execute(query, *values)

async def delete_banner(id):
    async with (await get_db()).acquire() as conn:
        item = await conn.fetchrow("SELECT * FROM user_banners WHERE id = ?", id)
        if not item:
            raise NotFoundError
        query = """
        DELETE FROM user_banners
            WHERE id = ?
        """
        await conn.execute(query, id)
