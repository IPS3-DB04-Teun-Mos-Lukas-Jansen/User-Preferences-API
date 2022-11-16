from fastapi import HTTPException
import pytest
import uuid
import auth
from models.LayoutModels import Card
from models.TokenModel import verified_token
from datetime import datetime, timedelta
import mongomock



def init_mock_layout_db(dummy_card_id, dummy_user_id):
    collection_mock = mongomock.MongoClient().mocklayout_db.mocklayout_collection
    auth.layoutdb = collection_mock

    card_obj = Card(cardId= dummy_card_id, cardType="url")
    collection_mock.update_one({"userId": dummy_user_id } ,{'$push': {'columns.0.cards': dict(card_obj)}}, upsert = True )

def mock_init(mock_user_id):
    def mock_verify_oauth2_token( token, request, client_id):
        return {"sub": mock_user_id}
    auth.id_token.verify_oauth2_token = mock_verify_oauth2_token
    auth.verified_tokens = []

def mock_init_shouldfail():
    def mock_verify_oauth2_token( token, request, client_id):
        raise ValueError("Invalid token")
    auth.id_token.verify_oauth2_token = mock_verify_oauth2_token
    auth.verified_tokens = []



def test_verify_token_returns_userid():
    #arrange
    user_id = str(uuid.uuid4()) 
    mock_init(user_id)

    #act
    result = auth.verify_token("dummy_token")

    #assert
    assert result == user_id
    assert len(auth.verified_tokens) == 1
    assert auth.verified_tokens[0].user_id == user_id

def test_verify_token_raises_httperror():
    #arrange
    mock_init_shouldfail()

    #act/assert
    with pytest.raises(HTTPException):
        auth.verify_token("dummy_token")

    #assert
    assert len(auth.verified_tokens) == 0

def test_verify_token_when_already_exists_should_return_userid():
    #arrange
    user_id = str(uuid.uuid4()) 
    mock_init(user_id)
    dummy_token = "dummy_token"

    #act
    result = auth.verify_token(dummy_token)
    result = auth.verify_token(dummy_token)

    #assert
    assert result == user_id
    assert len(auth.verified_tokens) == 1
    assert auth.verified_tokens[0].user_id == user_id


def test_is_token_verified_when_exists_should_return_token():
    #arrange
    user_id = str(uuid.uuid4()) 
    mock_init(user_id)
    dummy_token = "dummy_token"
    dummy_token_date = datetime.now()
    dummy_token_obj = verified_token(id_token=dummy_token, verified_date_time=dummy_token_date, user_id=user_id)
    auth.verified_tokens.append(dummy_token_obj)

    #act
    result = auth.is_token_verified(dummy_token)

    #assert
    assert result != None
    assert result.id_token == dummy_token
    assert result.verified_date_time == dummy_token_date
    assert result.user_id == user_id

def test_is_token_verified_when_not_exists_should_return_none():
    #arrange
    user_id = str(uuid.uuid4()) 
    mock_init(user_id)
    dummy_token = "dummy_token"
    dummy_token = "dummy_token2"
    dummy_token2_date = datetime.now()

    dummy_token2_obj = verified_token(id_token=dummy_token, verified_date_time=dummy_token2_date, user_id=user_id)
    auth.verified_tokens.append(dummy_token2_obj)

    #act
    result = auth.is_token_verified(dummy_token)

    #assert
    result == None

def test_remove_expired_tokens_should_only_remove_expired_tokens():
    #arrange
    
    user_id = str(uuid.uuid4()) 
    mock_init(user_id)
    dummy_token = "dummy_token"
    dummy_token_date = datetime.now()
    dummy_token_obj = verified_token(id_token=dummy_token, verified_date_time=dummy_token_date, user_id=user_id)

    user_id2 = str(uuid.uuid4()) 
    dummy_token2 = "dummy_token"
    dummy_token2_date = datetime.now() - timedelta(seconds=auth.token_expiration_time + 1)  
    dummy_token2_obj = verified_token(id_token=dummy_token2, verified_date_time=dummy_token2_date, user_id=user_id2)

    auth.verified_tokens.append(dummy_token_obj)
    auth.verified_tokens.append(dummy_token2_obj)

    #act
    auth.remove_expired_tokens()

    #assert
    assert len(auth.verified_tokens) == 1
    assert auth.verified_tokens[0].user_id == user_id
    assert auth.verified_tokens[0].id_token == dummy_token
    assert auth.verified_tokens[0].verified_date_time == dummy_token_date
    assert auth.verified_tokens[0].user_id != user_id2

def test_verify_urlcard_to_user_when_token_exists_should_return_true():
    #arrange
    user_id = str(uuid.uuid4()) 
    card_id = str(uuid.uuid4())
    mock_init(user_id)
    init_mock_layout_db(card_id, user_id)
    
    dummy_token = "dummy_token"

    #act
    result = auth.verify_urlcard_to_user(dummy_token, card_id)

    #assert
    assert result == True

def test_verify_urlcard_to_user_when_token_not_exists_should_raise_httpexeption():
    #arrange
    user_id = str(uuid.uuid4()) 
    card_id = str(uuid.uuid4())
    mock_init_shouldfail()
    init_mock_layout_db(card_id, user_id)

    #act/assert
    with pytest.raises(HTTPException) as ex:
        auth.verify_urlcard_to_user("dummy_token", card_id)

    assert ex.value.detail == "Invalid token"
    assert ex.value.status_code == 401

def test_verify_urlcard_to_user_when_card_not_exists_should_raise_httpexeption():
    #arrange
    user_id = str(uuid.uuid4()) 
    card_id = str(uuid.uuid4())
    card_id2 = str(uuid.uuid4())

    dummy_token = "dummy_token"
    mock_init(user_id)
    init_mock_layout_db(card_id, user_id)

    #act/assert
    with pytest.raises(HTTPException) as ex:
        auth.verify_urlcard_to_user(dummy_token, card_id2)

    #assert
    assert ex.value.detail == "Invalid user"
    assert ex.value.status_code == 401


