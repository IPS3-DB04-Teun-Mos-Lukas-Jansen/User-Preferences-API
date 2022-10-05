from tkinter.tix import COLUMN
from typing import List
from unittest import result
import uuid
from models.LayoutModels import Layout, Collumn, Card
from fastapi import APIRouter  ,HTTPException

from bson.json_util import dumps

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.layout
layoutdb = db.layout_collection


router = APIRouter()

# # # # # # # # # # #Create layout
# # # # # # # # # # @router.post("/api/v1/layout/{UserId}")
# # # # # # # # # # async def CreateLayout(UserId:str, collumnsAmount:int):

# # # # # # # # # #     card = Card(cardId=1,cardType=2)
# # # # # # # # # #     collumn = Collumn(cards=[card])
# # # # # # # # # #     collumnList = [collumn] * collumnsAmount
# # # # # # # # # #     print(collumn)
# # # # # # # # # #     layoutObject = Layout(userId=UserId, collumns=collumnList)
# # # # # # # # # #     layoutObjectDict = dict(layoutObject)
# # # # # # # # # #     #layoutdb.insert_one(dict(layoutObject))


    


#Get layout by userId 


#Add Column

#Remove Column


#add card to column
@router.post("/api/v1/layout/card/{UserId}")
async def AddCard(UserId:str, collumnNumber:int, type: str):

    id = str(uuid.uuid4())
    rows = layoutdb.update_one({"userId": UserId } ,{'$push': {'columns.'+ str(collumnNumber)+'.cards': dict(Card(cardId= id, cardType=type))}}, upsert = True )
    return str(rows.modified_count); 

#remove card from column
@router.delete("/api/v1/layout/card/{UserId}")
async def RemoveCard(UserId:str, collumnNumber:int, cardId:str):
        rows = layoutdb.update_one({"userId": UserId } ,{'$pull': {'columns.'+ str(collumnNumber)+'.cards': { "cardId" : cardId} } } )
        return str(rows.modified_count)
