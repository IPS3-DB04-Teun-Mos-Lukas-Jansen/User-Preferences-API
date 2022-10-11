import json
import uuid
from fastapi import APIRouter  ,HTTPException

from bson.json_util import dumps

from pymongo import MongoClient

from models.UrlModels import UrlCard

client = MongoClient('mongodb://localhost:27017/')
db = client.urlcards
urldb = db.urlcards_collection


router = APIRouter()

#Add urlcard
@router.post("")
async def AddUrlCard():
    id = str(uuid.uuid4())
    urlcard = UrlCard(cardId=id)
    urldb.insert_one(dict(urlcard))
    return id
    

#remove urlcard
@router.delete("/{cardId}")
async def RemoveUrlCard(cardId: str):
    rows = urldb.delete_one({"cardId": cardId})
    return str(rows.deleted_count)

#add url to card

#remove url from card

#update url in card

