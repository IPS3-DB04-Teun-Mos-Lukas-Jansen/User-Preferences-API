import uuid
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional
from typing import List


class Url(BaseModel):
    urlId: str
    url: str

class UrlCard(BaseModel):
    cardId: str
    urls: Optional[List[Url]]