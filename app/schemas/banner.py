from datetime import datetime
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


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass


class Banner(BannerBase):
    created_at: str
    updated_at: str
