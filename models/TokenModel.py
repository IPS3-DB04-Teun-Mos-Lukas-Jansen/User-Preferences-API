from pydantic import BaseModel
from datetime import datetime

class verified_token(BaseModel):
    id_token: str
    verified_date_time: datetime 
    user_id: str