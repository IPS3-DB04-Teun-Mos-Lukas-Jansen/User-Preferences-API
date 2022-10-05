import imp
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI  ,HTTPException

from routers import layout


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


app.include_router(layout.router)



        

