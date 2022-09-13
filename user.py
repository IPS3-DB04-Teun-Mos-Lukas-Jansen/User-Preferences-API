import uuid
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional


class User(BaseModel):
    id: str
    email_adress: str
    first_name: str
    last: str
    middle_name: Optional[str]