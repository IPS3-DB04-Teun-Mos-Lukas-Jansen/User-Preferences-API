from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import urls


from models.UrlModels import UrlList, Url

from fastapi import FastAPI  ,HTTPException


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(urls.router)



        

