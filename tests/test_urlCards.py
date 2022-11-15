import pytest
import uuid
from routers import urlCards
import mongomock
from models.UrlModels import UrlCard, Url

collection_mock = mongomock.MongoClient().mockurl_db.mockurl_collection

def create_mock_db():
    urlCards.urldb = collection_mock


@pytest.mark.asyncio
async def test_get_card_returns_correct_card():

    #arrange
    create_mock_db()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), Urls=[])
    collection_mock.insert_one(dict(urlcard))

    #act
    result = await urlCards.get_card(urlcard.cardId)
    
    #assert
    assert result != None
    assert urlcard.cardId == result["cardId"]
    assert urlcard.urls == result["urls"]

@pytest.mark.asyncio
async def test_add_url_card_adds_card_to_db():

    #arrange
    create_mock_db()

    #act
    card_id = await urlCards.add_url_card()
    result = collection_mock.find_one({"cardId": card_id })

    #assert
    assert result != None
    assert card_id == result["cardId"]

@pytest.mark.asyncio
async def test_remove_url_card_removes_card_from_db():
    #arrange
    create_mock_db()
    url_card = UrlCard(cardId=str(uuid.uuid4()), urls=[])
    collection_mock.insert_one(dict(url_card))

    #act
    pre_result = collection_mock.find_one({"cardId": url_card.cardId })
    rows = await urlCards.remove_url_card(url_card.cardId)
    result = collection_mock.find_one({"cardId": url_card.cardId })

    #assert
    assert pre_result["cardId"] == url_card.cardId
    assert pre_result != None
    assert rows == str(1)
    assert result == None

@pytest.mark.asyncio
async def test_add_url_to_card_adds_url_to_card_in_db():
    #arrange
    create_mock_db()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), urls=[])
    collection_mock.insert_one(dict(urlcard))

    url = "https://kanikeenkortebroekaan.nl/"

    #act
    url_id = await urlCards.add_url_to_card(urlcard.cardId, url)
    url_id2 = await urlCards.add_url_to_card(urlcard.cardId, url)

    urlcard_after = collection_mock.find_one({"cardId": urlcard.cardId })
    #assert
    assert urlcard_after != None
    assert len(urlcard_after["urls"]) == 2
    assert urlcard_after["urls"][0]["url"] == url
    assert urlcard_after["urls"][0]["urlId"] == url_id
    assert urlcard_after["urls"][1]["url"] == url
    assert urlcard_after["urls"][1]["urlId"] == url_id2

@pytest.mark.asyncio
async def test_remove_url_from_card_removes_url_from_card_in_db():
    #arrange
    create_mock_db()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), urls=[])
    collection_mock.insert_one(dict(urlcard))

    urlobject = Url(urlId=str(uuid.uuid4), url="https://kanikeenkortebroekaan.nl/")
    
    collection_mock.update_one({"cardId": urlcard.cardId}, {"$push":{"urls":dict(urlobject)} })

    #act

    urlcard_before = collection_mock.find_one({"cardId": urlcard.cardId })
    rows = await urlCards.remove_url_from_card(urlcard.cardId, urlobject.urlId)
    urlcard_after = collection_mock.find_one({"cardId": urlcard.cardId })

    #assert
    assert urlcard_after != None
    assert rows == str(1)
    assert len(urlcard_after["urls"]) == 0
    assert len(urlcard_before["urls"]) == 1

@pytest.mark.asyncio
async def test_update_url_in_card_updates_url_in_card_in_db():
    #arrange
    create_mock_db()
    urlcard = UrlCard(cardId=str(uuid.uuid4()), urls=[])
    collection_mock.insert_one(dict(urlcard))

    urlobject = Url(urlId=str(uuid.uuid4), url="https://kanikeenkortebroekaan.nl/")
    
    collection_mock.update_one({"cardId": urlcard.cardId}, {"$push":{"urls":dict(urlobject)} })

    new_url = "https://minecraft.net/"
    #act

    urlcard_before = collection_mock.find_one({"cardId": urlcard.cardId })
    rows = await urlCards.update_url_in_card(urlcard.cardId, urlobject.urlId, new_url)
    urlcard_after = collection_mock.find_one({"cardId": urlcard.cardId })

    #assert
    assert urlcard_after != None
    assert rows == str(1)
    assert len(urlcard_after["urls"]) == 1
    assert urlcard_after["urls"][0]["urlId"] ==  urlobject.urlId
    assert urlcard_before != urlcard_after
    assert urlcard_before["urls"][0]["url"] == urlobject.url
    assert urlcard_after["urls"][0]["url"] == new_url




