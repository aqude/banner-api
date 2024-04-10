from datetime import datetime
from typing import List

from app.api.core.database import get_db
from app.exceptions import NotFoundError
from app.schemas.banner import BannerCreate, BannerUpdate, Banner, Content


async def get_banner_for_user(tag_id, feature_id, use_last_revision, token):
    async with (await get_db()).acquire() as conn:
        check_active_status = """
        SELECT title, text, url FROM user_banners
        WHERE user_token = $1 AND is_active = TRUE
        """
        check = await conn.fetchval(check_active_status, token)
        if check:
            raise NotFoundError
        use_last_revision_query = """
        SELECT title, text, url FROM user_banners
            WHERE tag_ids @> $1 AND feature_id = $2 AND user_token = $3
            ORDER BY title DESC
            LIMIT 1
        """
        else_query = """
        SELECT title, text, url FROM user_banners
            WHERE tag_ids @> $1 AND feature_id = $2 AND user_token = $3
        """
        if use_last_revision:
            query = use_last_revision_query
            values = ([tag_id], feature_id, token)
        else:
            query = else_query
            values = ([tag_id], feature_id, token)
        banner = await conn.fetchrow(query, *values)
        banner = Content(**banner)
        if banner:
            return banner
        else:
            raise NotFoundError


async def get_all_banners(feature_id, tag_id, limit, offset) -> List[Banner]:
    async with (await get_db()).acquire() as conn:
        # НЕБЕЗОПАСНЫЙ КОД!
        query = """
        SELECT id as banner_id, tag_ids, feature_id, title, text, url, is_active, created_at, updated_at 
        FROM user_banners
        WHERE 1=1
        """
        args = []

        if feature_id is not None:
            query += " AND feature_id = ${}"
            args.append(feature_id)

        if tag_id is not None:
            query += f" AND tag_ids @> ${{}}"
            args.append([tag_id])

        if limit is not None:
            query += " LIMIT ${}"
            args.append(limit)

        if offset is not None:
            query += " OFFSET ${}"
            args.append(offset)

        # after we defined our arguments, we replace placeholder-parameters by correct ones
        query = query.format(*range(1, len(args) + 1))

        banners = await conn.fetch(query, *args)
        banners_objects = []
        for banner in banners:
            content = Content(
                title=banner['title'],
                text=banner['text'],
                url=banner['url']
            )
            banner_object = Banner(
                banner_id=banner['banner_id'],
                tag_ids=banner['tag_ids'],
                feature_id=banner['feature_id'],
                content=content,
                is_active=banner['is_active'],
                created_at=str(banner['created_at'].isoformat()),
                updated_at=str(banner['updated_at'].isoformat())
            )
            banners_objects.append(banner_object)
        banners = banners_objects
        return banners


async def create_banner(banner: BannerCreate):
    async with (await get_db()).acquire() as conn:
        query = """
            INSERT INTO user_banners
                (tag_ids, feature_id, title, text, url, is_active, created_at, updated_at)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """

        values = (
            banner.tag_ids,
            banner.feature_id,
            banner.content.title,
            banner.content.text,
            banner.content.url,
            banner.is_active,
            datetime.now(),
            datetime.now(),
        )
        banner_id = await conn.fetchval(query, *values)
        return str(banner_id)


async def update_banner(id, banner: BannerUpdate):
    async with (await get_db()).acquire() as conn:
        check = await conn.fetchrow("SELECT * FROM user_banners WHERE id = $1", id)
        if not check:
            raise NotFoundError
        query = """
        UPDATE user_banners
            SET title = $1, text = $2, url = $3, is_active = $4, updated_at = $5
        WHERE id = $6
        """
        values = (banner.content.title, banner.content.text, banner.content.url, banner.is_active, datetime.now(), id)
        item = await conn.execute(query, *values)

        return item


async def delete_banner(id: int):
    async with (await get_db()).acquire() as conn:
        check = await conn.fetchrow("SELECT * FROM user_banners WHERE id = $1", id)
        if not check:
            raise NotFoundError
        item = await conn.execute("DELETE FROM user_banners WHERE id = $1", id)
        return item
