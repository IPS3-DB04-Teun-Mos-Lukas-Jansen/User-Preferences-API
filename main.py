from user import User
from fastapi import FastAPI  ,HTTPException
from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client.users
userdb = db.user_collection


@app.post("/api/v1/user/create")
async def register_user(user: User):

    exists = await get_user_by_id(user.id)

    if len(exists) is not 4:
        raise HTTPException(status_code=418, detail="User already exists")
    else:
        id = userdb.insert_one(dict(user))
        return str(id)
        

@app.get("/api/v1/user/{userid}")
async def get_user_by_id(userid:str):
    user = userdb.find_one({"id": userid })
    return str(user)

@app.put("/api/v1/user/{userid}")
async def update_user_by_id(user: User , userid:str):
    status = userdb.update_one({"id": userid } ,{ '$set' : dict(user) } )
    return str(status.modified_count)

@app.delete("/api/v1/user/{userid}")
async def delete_user_by_id(userid:str):
    status = userdb.delete_one({"id": userid })
    return str(status.deleted_count)