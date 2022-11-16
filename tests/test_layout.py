import pytest
import uuid
from routers import layout
import mongomock
from models.LayoutModels import Card

collection_mock = mongomock.MongoClient().mocklayout_db.mocklayout_collection

def mock_init(mock_user_id):
    layout.layoutdb = collection_mock

    def verify_token_mock(token:str):
        return mock_user_id
    layout.verify_token = verify_token_mock



@pytest.mark.asyncio
async def test_get_layout_returns_correctlayout():
    #arrange
    user_id = str(uuid.uuid4()) 
    column_number = 0
    card_id = str(uuid.uuid4()) 
    card_type = "url"
    mock_init(user_id)

    collection_mock.update_one({"userId": user_id } ,{'$push': {'columns.'+ str(column_number)+'.cards': dict(Card(cardId= card_id, cardType=card_type))}}, upsert = True )
    
    
    #act
    result_layout = await layout.get_layout("dummy_token")

    #assert
    assert result_layout != None
    assert result_layout["userId"] == user_id
    assert result_layout["columns"]["0"]['cards'][0]["cardId"] == card_id

@pytest.mark.asyncio
async def test_remove_column_removes_column_from_db():
    #arrange
    user_id = str(uuid.uuid4()) 
    column_number = 0
    card_id = str(uuid.uuid4()) 
    card_type = "url"
    mock_init(user_id)

    collection_mock.update_one({"userId": user_id } ,{'$push': {'columns.'+ str(column_number)+'.cards': dict(Card(cardId= card_id, cardType=card_type))}}, upsert = True )
    
    #act
    layout_before = collection_mock.find_one({"userId": user_id })
    rows = await layout.remove_column("dummy_token", column_number)
    layout_after = collection_mock.find_one({"userId": user_id })

    #assert
    assert layout_before["columns"]["0"]['cards'][0]["cardId"] == card_id
    assert layout_after != None
    assert layout_after["columns"] == {}
    assert rows == str(1)

@pytest.mark.asyncio
async def test_add_card_adds_card_to_db():
    #arrange
    user_id = str(uuid.uuid4()) 
    column_number = 0
    card_id = str(uuid.uuid4()) 
    card_type = "url"
    mock_init(user_id)

    #act
    layout_before = collection_mock.find_one({"userId": user_id })
    await layout.add_card("dummy_token", column_number, card_id, card_type)
    layout_after = collection_mock.find_one({"userId": user_id })

    #assert
    assert layout_before ==  None
    assert layout_after["columns"]["0"]['cards'][0]["cardId"] == card_id
    assert len(layout_after["columns"]["0"]['cards']) == 1

@pytest.mark.asyncio
async def test_remove_card_removes_card_from_db():
    #arrange
    user_id = str(uuid.uuid4()) 
    column_number = 0
    card_id = str(uuid.uuid4()) 
    card_type = "url"
    mock_init(user_id)

    collection_mock.update_one({"userId": user_id } ,{'$push': {'columns.'+ str(column_number)+'.cards': dict(Card(cardId= card_id, cardType=card_type))}}, upsert = True )
    
    #act
    layout_before = collection_mock.find_one({"userId": user_id })
    await layout.remove_card("dummy_token", column_number, card_id)
    layout_after = collection_mock.find_one({"userId": user_id })

    #assert
    assert layout_after != None
    assert layout_before["columns"]["0"]['cards'][0]["cardId"] == card_id
    assert len(layout_after["columns"]["0"]['cards']) == 0
