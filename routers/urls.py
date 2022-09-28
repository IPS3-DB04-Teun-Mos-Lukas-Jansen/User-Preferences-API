from models.UrlModels import UrlList, Url
from fastapi import APIRouter  ,HTTPException

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.urls
urldb = db.urls_collection


router = APIRouter()





#add 1 url
@router.post("/api/v1/url/{userid}")
async def add_url(url: Url, userid: str):
        id = urldb.update_one({"id": userid } ,{'$push': {'urls': dict(url)}}, upsert = True )
        return str(id.modified_count)
        
#remove 1 url
@router.delete("/api/v1/url/{userid}")
async def remove_url(urlid: str, userid: str):
        id = urldb.update_one({"id": userid } ,{'$pull': {'urls': { "UrlId" : urlid} } } )
        return str(id.modified_count)

#get all urls from 1 user
@router.get("/api/v1/url/{userid}")
async def get_urls(userid: str):
        urllist = urldb.find_one({"id": userid })
        return str(urllist)


#update 1 url
@router.put("/api/v1/url/{userid}")
async def update_url(url: Url, userid: str):
        id = urldb.update_one({"id": userid, "urls.UrlId" : url.UrlId} ,{'$set': {'urls.$':  dict(url) } } )
        return str(id.modified_count)


#get url by id?????