import uuid
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional
from typing import List

class Url(BaseModel):
    UrlId: str
    Url: str

class UrlList(BaseModel):
    UserId: str
    Urls: List[Url]
    