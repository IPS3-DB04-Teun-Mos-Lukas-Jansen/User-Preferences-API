from fastapi import Depends, FastAPI


from routers import urls


from models.UrlModels import UrlList, Url

from fastapi import FastAPI  ,HTTPException


app = FastAPI()

app.include_router(urls.router)



        

