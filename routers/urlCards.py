import json
import uuid
from models.UrlModels import Url
from fastapi import APIRouter ,HTTPException

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
    urlcard = UrlCard(cardId=id, Urls=[])
    urldb.insert_one(dict(urlcard))
    return id
    

#remove urlcard
@router.delete("/{cardId}")
async def RemoveUrlCard(cardId: str):
    rows = urldb.delete_one({"cardId": cardId})
    return str(rows.deleted_count)

#add url to card
@router.post("/{cardId}/url")
async def AddUrlToCard(cardId:str, url:str):
    id = str(uuid.uuid4())
    urlobject = Url(UrlId=id, Url=url)
    urldb.update_one({"cardId": cardId}, {"$push":{"Urls":dict(urlobject)} })
    return id


#remove url from card
@router.delete("/{cardId}/url")
async def RemoveUrlFromCard(cardId:str, urlId: str):
    rows = urldb.update_one({"cardId": cardId } ,{'$pull': {'Urls': { "UrlId" : urlId} } } )
    return str(rows.modified_count)

#update url in card
@router.put("/{cardId}/url")
async def UpdateUrlInCard(cardId:str, urlId: str, newUrl: str):
    urlObject = Url( UrlId = urlId , Url = newUrl)
    id = urldb.update_one({"cardId": cardId, "Urls.UrlId" : urlObject.UrlId} ,{'$set': {'Urls.$':  dict(urlObject) } } )
    return str(id.modified_count)

