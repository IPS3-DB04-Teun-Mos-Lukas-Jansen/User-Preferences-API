import pytest
from routers import urlCards
import mongomock

def createMockDB():
    collection_mock = mongomock.MongoClient().mockurl_db.mockurl_collection
    urlCards.urldb = collection_mock


@pytest.mark.asyncio
async def test():
    createMockDB()
    assert 0 == await urlCards.AddUrlCard()