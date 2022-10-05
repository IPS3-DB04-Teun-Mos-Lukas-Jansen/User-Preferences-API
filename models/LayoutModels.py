from pydantic import BaseModel
from typing import Optional
from typing import List

class Card(BaseModel):
    cardId: str
    cardType: str 

class Collumn(BaseModel):
    cards :  List[Card]

class Layout(BaseModel):
    userId: str
    collumns: List[Collumn]
