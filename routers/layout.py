from typing import List
import uuid
from models.LayoutModels import Layout, Collumn, Card
from fastapi import APIRouter
import json
from bson.json_util import dumps
from pymongo import MongoClient
import os


DB_URL = os.environ.get('USER_PREF_DB_URL')

client = MongoClient(DB_URL)
db = client.layout
layoutdb = db.layout_collection

router = APIRouter()

#Get layout by userId 
@router.get("/{UserId}")
async def GetLayout(UserId:str):
    layout = layoutdb.find_one({"userId": UserId })
    
    return json.loads(dumps(layout))

#Remove Column
@router.delete("/column/{UserId}")
async def RemoveColumn(UserId:str, collumnNumber:int):
    rows = layoutdb.update_one({"userId": UserId}, {'$unset':{'columns.' + str(collumnNumber): 1 }})
    
    return str(rows.modified_count)

#add card to column
@router.post("/card/{UserId}")
async def AddCard(UserId:str, collumnNumber:int, type: str):

    id = str(uuid.uuid4())
    rows = layoutdb.update_one({"userId": UserId } ,{'$push': {'columns.'+ str(collumnNumber)+'.cards': dict(Card(cardId= id, cardType=type))}}, upsert = True )
    return str(rows.modified_count); 

#remove card from column
@router.delete("/card/{UserId}")
async def RemoveCard(UserId:str, collumnNumber:int, cardId:str):
        rows = layoutdb.update_one({"userId": UserId } ,{'$pull': {'columns.'+ str(collumnNumber)+'.cards': { "cardId" : cardId} } } )
        return str(rows.modified_count)
