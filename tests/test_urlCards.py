import pytest
import uuid
import json
from routers import urlCards
import mongomock
from models.UrlModels import UrlCard

collection_mock = mongomock.MongoClient().mockurl_db.mockurl_collection

def createMockDB():
    urlCards.urldb = collection_mock


@pytest.mark.asyncio
async def test_GetCard_returns_CorrectCard():

    #arrange
    createMockDB()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    #act
    result = await urlCards.GetCard(urlcard.cardId)
    
    #assert
    assert result != None
    assert urlcard.cardId == result["cardId"]
    assert urlcard.Urls == result["Urls"]