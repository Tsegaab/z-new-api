from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Base(BaseModel):
    id: int
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True


class News(BaseModel):
    headline: str
    link: str
    source: str
    image_url: Union[None, str] = None
