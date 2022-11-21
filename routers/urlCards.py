import json
import uuid
from auth import verify_urlcard_to_user, verify_token
from models.UrlModels import Url
from fastapi import APIRouter ,HTTPException

from bson.json_util import dumps

from pymongo import MongoClient

from models.UrlModels import UrlCard
import os

DB_URL = os.environ.get('USER_PREF_DB_URL')

client = MongoClient(DB_URL)
db = client.urlcards
urldb = db.urlcards_collection


router = APIRouter()

#Get card by card_id 
@router.get("/{token}")
async def get_card(token:str, card_id:str):
    verify_urlcard_to_user(token, card_id)

    card = urldb.find_one({"cardId": card_id })
    return json.loads(dumps(card))


#Add urlcard
@router.post("/{token}")
async def add_url_card(token:str):
    verify_token(token)

    card_id = str(uuid.uuid4())
    url_card = UrlCard(cardId=card_id, urls=[])
    urldb.insert_one(dict(url_card))
    return card_id
    

#remove urlcard
@router.delete("/{token}")
async def remove_url_card(token:str, card_id: str):
    verify_urlcard_to_user(token, card_id)
    rows = urldb.delete_one({"cardId": card_id})
    return str(rows.deleted_count)

#add url to card
@router.post("/{token}/url")
async def add_url_to_card(token:str,card_id:str, url:str):
    verify_urlcard_to_user(token, card_id)
    url_id = str(uuid.uuid4())
    url_object = Url(urlId=url_id, url=url)
    urldb.update_one({"cardId": card_id}, {"$push":{'urls':dict(url_object)} })
    return url_id

#remove url from card
@router.delete("/{token}/url")
async def remove_url_from_card(token:str,card_id:str, url_id: str):
    verify_urlcard_to_user(token, card_id)
    rows = urldb.update_one({"cardId": card_id } ,{'$pull': {'urls': { 'urlId' : url_id} } } )
    return str(rows.modified_count)

#update url in card
@router.put("/{token}/url")
async def update_url_in_card(token:str,card_id:str, url_id: str, new_url: str):
    verify_urlcard_to_user(token, card_id)
    url_object = Url( urlId = url_id , url = new_url)
    rows = urldb.update_one({"cardId": card_id, "urls.urlId" : url_object.urlId} ,{'$set': {'urls.$':  dict(url_object) } } )
    return str(rows.modified_count)

