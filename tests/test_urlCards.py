import pytest
import uuid
from routers import urlCards
import mongomock
from models.UrlModels import UrlCard, Url

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

@pytest.mark.asyncio
async def test_AddUrlCard_Adds_card_to_db():

    #arrange
    createMockDB()

    #act
    id = await urlCards.AddUrlCard()
    result = collection_mock.find_one({"cardId": id })

    #assert
    assert result != None
    assert id == result["cardId"]

@pytest.mark.asyncio
async def test_RemoveUrlCard_Removes_card_from_db():
    #arrange
    createMockDB()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    #act
    preResult = collection_mock.find_one({"cardId": urlcard.cardId })
    rows = await urlCards.RemoveUrlCard(urlcard.cardId)
    result = collection_mock.find_one({"cardId": urlcard.cardId })

    #assert
    assert preResult["cardId"] == urlcard.cardId
    assert preResult != None
    assert rows == str(1)
    assert result == None

@pytest.mark.asyncio
async def test_AddUrlToCard_adds_url_to_card_in_db():
    #arrange
    createMockDB()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    url = "https://kanikeenkortebroekaan.nl/"

    #act
    urlId = await urlCards.AddUrlToCard(urlcard.cardId, url)
    urlId2 = await urlCards.AddUrlToCard(urlcard.cardId, url)

    urlcardAfter = collection_mock.find_one({"cardId": urlcard.cardId })
    #assert
    assert urlcardAfter != None
    assert len(urlcardAfter["Urls"]) == 2
    assert urlcardAfter["Urls"][0]["Url"] == url
    assert urlcardAfter["Urls"][0]["UrlId"] == urlId
    assert urlcardAfter["Urls"][1]["Url"] == url
    assert urlcardAfter["Urls"][1]["UrlId"] == urlId2

@pytest.mark.asyncio
async def test_RemoveUrlFromCard_removes_url_from_card_in_db():
    #arrange
    createMockDB()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    urlobject = Url(UrlId=str(uuid.uuid4), Url="https://kanikeenkortebroekaan.nl/")
    
    collection_mock.update_one({"cardId": urlcard.cardId}, {"$push":{"Urls":dict(urlobject)} })

    #act

    urlcardBefore = collection_mock.find_one({"cardId": urlcard.cardId })
    rows = await urlCards.RemoveUrlFromCard(urlcard.cardId, urlobject.UrlId)
    urlcardAfter = collection_mock.find_one({"cardId": urlcard.cardId })

    #assert
    assert urlcardAfter != None
    assert rows == str(1)
    assert len(urlcardAfter["Urls"]) == 0
    assert len(urlcardBefore["Urls"]) == 1

@pytest.mark.asyncio
async def test_UpdateUrlInCard_updates_url_in_card_in_db():
    #arrange
    createMockDB()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    urlobject = Url(UrlId=str(uuid.uuid4), Url="https://kanikeenkortebroekaan.nl/")
    
    collection_mock.update_one({"cardId": urlcard.cardId}, {"$push":{"Urls":dict(urlobject)} })

    newUrl = "https://minecraft.net/"
    #act

    urlcardBefore = collection_mock.find_one({"cardId": urlcard.cardId })
    rows = await urlCards.UpdateUrlInCard(urlcard.cardId, urlobject.UrlId, newUrl)
    urlcardAfter = collection_mock.find_one({"cardId": urlcard.cardId })

    #assert
    assert urlcardAfter != None
    assert rows == str(1)
    assert len(urlcardAfter["Urls"]) == 1
    assert urlcardAfter["Urls"][0]["UrlId"] ==  urlobject.UrlId
    assert urlcardBefore != urlcardAfter
    assert urlcardBefore["Urls"][0]["Url"] == urlobject.Url
    assert urlcardAfter["Urls"][0]["Url"] == newUrl





