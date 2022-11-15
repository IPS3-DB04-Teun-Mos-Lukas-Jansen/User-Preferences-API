""" This file is responsible for layout endpoints """
import json
import os

from bson.json_util import dumps
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from auth import verify_token

from models.LayoutModels import Card

DB_URL = os.environ.get('USER_PREF_DB_URL')

client = MongoClient(DB_URL)
db = client.layout

layoutdb = db.layout_collection



router = APIRouter()

#Get layout by userId
@router.get("/{token}")
async def get_layout(token:str):
    user_id = verify_token(token)

    layout = layoutdb.find_one({"userId": user_id })
    return json.loads(dumps(layout))

#Remove Column
@router.delete("/column/{token}")
async def remove_column(token:str, column_number:int):
    user_id = verify_token(token)
    rows = layoutdb.update_one({"userId": user_id}, {'$unset':{'columns.' + str(column_number): 1 }})
    
    return str(rows.modified_count)

#add card to column
@router.post("/card/{token}")
async def add_card(token:str, column_number:int, card_id:str, type: str):
    user_id = verify_token(token)
    rows = layoutdb.update_one({"userId": user_id } ,{'$push': {'columns.'+ str(column_number)+'.cards': dict(Card(cardId= card_id, cardType=type))}}, upsert = True )
    return str(rows.modified_count); 

#remove card from column
@router.delete("/card/{token}")
async def remove_card(token:str, column_number:int, card_id:str):
    user_id = verify_token(token)
    rows = layoutdb.update_one({"userId": user_id } ,{'$pull': {'columns.'+ str(column_number)+'.cards': { "cardId" : card_id} } } )
    return str(rows.modified_count)




