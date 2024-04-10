from typing import Optional, List, Type

from fastapi import APIRouter, HTTPException, Header

from app.api.dependencies import authenticate_user_token, authenticate_admin_token
from app.crud.banner import get_banner_for_user, create_banner, update_banner, get_all_banners, delete_banner
from app.exceptions import AuthenticationError, NotFoundError
from app.logger.logger import Logger
from app.schemas.banner import BannerCreate, BannerUpdate, Banner
from app.schemas.response import Response

router = APIRouter()
logger = Logger()


@router.get("/user_banner")
async def get_user_banner(tag_id: int, feature_id: int, use_last_revision: bool = False,
                          token: str = Header(None)):
    try:
        authenticate_user_token(token)
        banner = await get_banner_for_user(tag_id, feature_id, use_last_revision, token)
        if banner:
            return banner
        else:
            raise HTTPException(status_code=404, detail="Баннер для пользователя не найден")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        logger.log_error(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/banner", status_code=200)
async def read_banners(token: str = Header(None), feature_id: int = None, tag_id: int = None,
                       limit: int = None, offset: int = None):
    try:
        authenticate_admin_token(token)
        banners = await get_all_banners(feature_id, tag_id, limit, offset)
        return banners
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        logger.log_error(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/banner")
async def create_new_banner(banner: BannerCreate, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        banner_id = await create_banner(banner)
        return {"banner_id": banner_id}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        logger.log_error(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/banner/{id}", status_code=200)
async def update_banner_info(id: int, banner: BannerUpdate, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        await update_banner(id, banner)
        return Response(status_code=200, detail="Баннер успешно обновлен")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    except Exception as e:
        logger.log_error(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.delete("/banner/{id}", status_code=204)
async def delete_banner_by_id(id: int, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        await delete_banner(id)
        return Response(status_code=204, detail="Баннер успешно удален")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    except Exception as e:
        logger.log_error(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
