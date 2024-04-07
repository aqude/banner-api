from typing import Optional

from fastapi import APIRouter, HTTPException, Header

from app.api.dependencies import authenticate_user_token, authenticate_admin_token
from app.crud.banner import get_banner_for_user, create_banner, update_banner, get_all_banners, delete_banner
from app.exceptions import AuthenticationError, NotFoundError
from app.schemas.banner import BannerCreate, BannerUpdate

router = APIRouter()


@router.get("/user_banner")
def get_user_banner(tag_id: int, feature_id: int, use_last_revision: bool = False, token: str = Header(None)):
    try:
        authenticate_user_token(token)
        banner = get_banner_for_user(tag_id, feature_id, use_last_revision)
        if banner:
            return banner
        else:
            raise HTTPException(status_code=404, detail="Баннер для пользователя не найден")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/banner")
def read_banners(token: str = Header(None), feature_id: Optional[int] = None, tag_id: Optional[int] = None,
                 limit: Optional[int] = None, offset: Optional[int] = None):
    try:
        authenticate_admin_token(token)
        banners = get_all_banners(feature_id, tag_id, limit, offset)
        return banners
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/banner", status_code=201)
def create_new_banner(banner: BannerCreate, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        banner_id = create_banner(banner)
        return {"banner_id": banner_id}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.patch("/banner/{id}")
def update_banner_info(id: int, banner: BannerUpdate, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        update_banner(id, banner)
        return {"message": "Баннер успешно обновлен"}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/banner/{id}")
def delete_banner_by_id(id: int, token: str = Header(None)):
    try:
        authenticate_admin_token(token)
        delete_banner(id)
        return {"message": "Баннер успешно удален"}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")