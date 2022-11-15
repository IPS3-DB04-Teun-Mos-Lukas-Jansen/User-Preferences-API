""" This file is responsible for layout endpoints """
import json
import os

from bson.json_util import dumps
from fastapi import APIRouter
from pymongo import MongoClient

from models.LayoutModels import Card

DB_URL = os.environ.get('USER_PREF_DB_URL')

client = MongoClient(DB_URL)
db = client.layout

layoutdb = db.layout_collection


router = APIRouter()

#Get layout by userId
@router.get("/{user_id}")
async def get_layout(user_id:str):
    layout = layoutdb.find_one({"userId": user_id })
    return json.loads(dumps(layout))

#Remove Column
@router.delete("/column/{user_id}")
async def remove_column(user_id:str, column_number:int):
    rows = layoutdb.update_one({"userId": user_id}, {'$unset':{'columns.' + str(column_number): 1 }})
    
    return str(rows.modified_count)

#add card to column
@router.post("/card/{user_id}")
async def add_card(user_id:str, column_number:int, card_id:str, type: str):
    rows = layoutdb.update_one({"userId": user_id } ,{'$push': {'columns.'+ str(column_number)+'.cards': dict(Card(cardId= card_id, cardType=type))}}, upsert = True )
    return str(rows.modified_count); 

#remove card from column
@router.delete("/card/{user_id}")
async def remove_card(user_id:str, column_number:int, card_id:str):
        rows = layoutdb.update_one({"userId": user_id } ,{'$pull': {'columns.'+ str(column_number)+'.cards': { "cardId" : card_id} } } )
        return str(rows.modified_count)
