from pydantic import BaseModel
from typing import Optional
from typing import List

class Card(BaseModel):
    cardId: str
    cardType: str 
    params: Optional[dict]

class Column(BaseModel):
    cards :  List[Card]

class Layout(BaseModel):
    userId: str
    collumns: List[Column]
