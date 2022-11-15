
from bson.json_util import dumps
import json
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
import os

from pymongo import MongoClient

CLIENT_ID = os.environ.get("REACT_APP_CLIENT_ID")


# token is the id_token from the client
def verify_token(token): 
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        userid = idinfo['sub']
        return userid
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

DB_URL = os.environ.get('USER_PREF_DB_URL')



def verify_urlcard_to_user(token, urlcard_id):
    user_id = verify_token(token)
    client = MongoClient(DB_URL)
    db = client.layout

    layoutdb = db.layout_collection
    print(user_id)
    layout = layoutdb.find_one({"userId": user_id })
    if "\"cardId\": \""+ urlcard_id + "\"," in dumps(layout):
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid user")

