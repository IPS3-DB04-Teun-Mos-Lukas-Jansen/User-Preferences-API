
from datetime import datetime
from bson.json_util import dumps
import json
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from models.TokenModel import verified_token

from pymongo import MongoClient

CLIENT_ID = os.environ.get("REACT_APP_CLIENT_ID")
DB_URL = os.environ.get('USER_PREF_DB_URL')

client = MongoClient(DB_URL)
db = client.layout
layoutdb = db.layout_collection

verified_tokens = []
token_expiration_time = (3600/2) # 30 minutes

# token is the id_token from the client
def verify_token(token): 
    
    token_obj = is_token_verified(token)
    
    if token_obj is None:
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            userid = idinfo['sub']
            token_obj = verified_token(id_token=token, verified_date_time=datetime.now(), user_id=userid)
            verified_tokens.append(token_obj)
            return userid
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        return token_obj.user_id


def is_token_verified(token):

    remove_expired_tokens()

    for verified_token in verified_tokens:
        if verified_token.id_token == token:
            return verified_token
    return None

def remove_expired_tokens():
    for verified_token in verified_tokens:
        if (datetime.now() - verified_token.verified_date_time).total_seconds() > token_expiration_time:
            verified_tokens.remove(verified_token)

def verify_urlcard_to_user(token, urlcard_id):
    user_id = verify_token(token)
    layout = layoutdb.find_one({"userId": user_id })
    if "\"cardId\": \""+ urlcard_id + "\"," in dumps(layout):
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid user")

