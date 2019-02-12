# -*- coding: utf-8 -*
from pymongo import MongoClient
import pytest

import tt_demo
from tt_demo.queries import Query

mongodb_uri = "mongodb://localhost:27017/mytest"

app = tt_demo.create_app("tt_demo",
                         mongodb_uri=mongodb_uri,
                         port=9090,
                         debug=False)


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c


def populate_db():
    """Add document in mycoll collection for tests"""
    client = MongoClient(mongodb_uri)

    # create document in mycoll
    for my_key in ("2017", "2018", "2019", "2020"):
        client.mytest.mycoll.delete_many({"domain": "test_domain_2", 
                                          "my_key": my_key})
        client.mytest.mycoll.insert_one({"domain": "test_domain_2",
                                         "my_key": my_key,
                                         "groupe": "a"})

    client.mytest.mycoll.insert_one({"domain": "test_domain_2", "my_key": "2020", "groupe": "b"})

    # create queries
    # ef9a570053038ba08b5ca89dac4a3a6c
    Query({"domain": "test_domain_2", "my_key": "2017"}).save()
    # 61dbb89ca5de54506143f3a7a07c2763
    Query({"domain": "test_domain_2", "my_key": "{{filter}}"}).save()
    # 66afee1fd2f6fb5d266a5944ae18e586
    Query([{"$match": {"domain": "test_domaine_2"}},
          {"$group": {"_id": "groupe"}}]).save()

populate_db()
