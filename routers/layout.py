from typing import List
import uuid
from models.LayoutModels import Layout, Collumn, Card
from fastapi import APIRouter
import json
from bson.json_util import dumps
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.layout
layoutdb = db.layout_collection

router = APIRouter()

#Get layout by userId 
@router.get("/{userId}")
async def GetLayout(userId:str):
    layout = layoutdb.find_one({"userId": userId })
    
    return json.loads(dumps(layout))

#Remove Column
@router.delete("/column/{userId}")
async def RemoveColumn(userId:str, columnNumber:int):
    rows = layoutdb.update_one({"userId": userId}, {'$unset':{'columns.' + str(columnNumber): 1 }})
    
    return str(rows.modified_count)

#add card to column
@router.post("/card/{userId}")
async def AddCard(userId:str, columnNumber:int, cardId:str, type: str):
    rows = layoutdb.update_one({"userId": userId } ,{'$push': {'columns.'+ str(columnNumber)+'.cards': dict(Card(cardId= cardId, cardType=type))}}, upsert = True )
    return str(rows.modified_count); 

#remove card from column
@router.delete("/card/{userId}")
async def RemoveCard(userId:str, columnNumber:int, cardId:str):
        rows = layoutdb.update_one({"userId": userId } ,{'$pull': {'columns.'+ str(columnNumber)+'.cards': { "cardId" : cardId} } } )
        return str(rows.modified_count)
