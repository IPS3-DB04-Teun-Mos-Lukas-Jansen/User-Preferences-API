from models.UrlModels import UrlList, Url

from fastapi import FastAPI  ,HTTPException
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.urls
urldb = db.urls_collection
#remove 1 url
#update 1 url


#get all urls

#get url by id?????


#add 1 url
# @app.post("/api/v1/url/create/{userid}")
# async def add_url(url: Url):

#         id = urldb.insert_one(dict(url))

#         return str(id)
# from pydantic import BaseModel
# from uuid import UUID, uuid4
# from typing import Optional
# from typing import List

# class Url(BaseModel):
#     UrlId: str
#     Url: str

# class UrlList(BaseModel):
#     UserId: str
#     Urls: List[Url]
    