import pytest
import uuid
from routers import layout
import mongomock
from models.LayoutModels import Layout, Card, Collumn

collection_mock = mongomock.MongoClient().mocklayout_db.mocklayout_collection

def createMockDB():
    layout.layoutdb = collection_mock


@pytest.mark.asyncio
async def test_GetLayout_returns_Correctlayout():
    #arrange
    createMockDB()
    userId = str(uuid.uuid4()) 
    columnNumber = 0
    cardId = str(uuid.uuid4()) 
    type = "url"

    collection_mock.update_one({"userId": userId } ,{'$push': {'columns.'+ str(columnNumber)+'.cards': dict(Card(cardId= cardId, cardType=type))}}, upsert = True )

    #act
    resultLayout = await layout.GetLayout(userId)

    #assert
    assert resultLayout != None
    assert resultLayout["userId"] == userId
    assert resultLayout["columns"]["0"]['cards'][0]["cardId"] == cardId

@pytest.mark.asyncio
async def test_RemoveColumn_Removes_column_from_db():
    #arrange
    createMockDB()
    userId = str(uuid.uuid4()) 
    columnNumber = 0
    cardId = str(uuid.uuid4()) 
    type = "url"

    collection_mock.update_one({"userId": userId } ,{'$push': {'columns.'+ str(columnNumber)+'.cards': dict(Card(cardId= cardId, cardType=type))}}, upsert = True )
    
    #act
    layoutBefore = collection_mock.find_one({"userId": userId })
    rows = await layout.RemoveColumn(userId, columnNumber)
    layoutAfter = collection_mock.find_one({"userId": userId })

    #assert
    assert layoutBefore["columns"]["0"]['cards'][0]["cardId"] == cardId
    assert layoutAfter != None
    assert layoutAfter["columns"] == {}
    assert rows == str(1)

@pytest.mark.asyncio
async def test_AddCard_adds_card_to_db():
    #arrange
    createMockDB()
    userId = str(uuid.uuid4()) 
    columnNumber = 0
    cardId = str(uuid.uuid4()) 
    type = "url"

    #act
    layoutBefore = collection_mock.find_one({"userId": userId })
    await layout.AddCard(userId, columnNumber, cardId, type)
    layoutAfter = collection_mock.find_one({"userId": userId })
    
    #assert
    assert layoutBefore ==  None
    assert layoutAfter["columns"]["0"]['cards'][0]["cardId"] == cardId
    assert len(layoutAfter["columns"]["0"]['cards']) == 1

@pytest.mark.asyncio
async def test_RemoveCard_removes_card_from_db():
    #arrange
    createMockDB()
    userId = str(uuid.uuid4()) 
    columnNumber = 0
    cardId = str(uuid.uuid4()) 
    type = "url"

    collection_mock.update_one({"userId": userId } ,{'$push': {'columns.'+ str(columnNumber)+'.cards': dict(Card(cardId= cardId, cardType=type))}}, upsert = True )
    
    #act
    layoutBefore = collection_mock.find_one({"userId": userId })
    await layout.RemoveCard(userId, columnNumber, cardId)
    layoutAfter = collection_mock.find_one({"userId": userId })

    #assert
    assert layoutAfter != None
    assert layoutBefore["columns"]["0"]['cards'][0]["cardId"] == cardId
    assert len(layoutAfter["columns"]["0"]['cards']) == 0
