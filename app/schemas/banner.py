from datetime import datetime
from typing import List

from pydantic import BaseModel


class Content(BaseModel):
    title: str
    text: str
    url: str


class BannerBase(BaseModel):
    tag_ids: List[int]
    feature_id: int
    content: Content
    is_active: bool


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass


class Banner(BannerBase):
    id: int
    created_at: datetime
    updated_at: datetime
