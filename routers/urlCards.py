import uuid
from fastapi import APIRouter  ,HTTPException

from bson.json_util import dumps

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.urlcards
urldb = db.urlcards_collection


router = APIRouter()


