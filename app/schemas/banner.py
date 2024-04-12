from typing import List

from pydantic import BaseModel


class Content(BaseModel):
    title: str
    text: str
    url: str


class BannerBase(BaseModel):
    banner_id: int
    tag_ids: List[int]
    feature_id: int
    content: Content
    is_active: bool


class BannerCreate(BaseModel):
    tag_ids: List[int]
    feature_id: int
    content: Content
    is_active: bool


class BannerUpdate(BannerBase):
    pass


class Banner(BannerBase):
    created_at: str
    updated_at: str
