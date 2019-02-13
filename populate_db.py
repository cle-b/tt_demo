# -*- coding: utf-8 -*
import os

import pymodm

from tt_demo.queries import Query


def populate_db():
    """Add document in mycoll collection and query for tests"""
    mongodb_uri = os.getenv("TT_MONGO_URI", "mongodb://localhost:27017/mytest")

    # connect to mongodb
    pymodm.connect(mongodb_uri)

    # create queries
    # ef9a570053038ba08b5ca89dac4a3a6c
    Query({"domain": "test_domain_2", "my_key": "2017"}).save()
    # 61dbb89ca5de54506143f3a7a07c2763
    Query({"domain": "test_domain_2", "my_key": "{{filter}}"}).save()
    # 89da2cbd2e566a77b0e96ebf06c26daf
    Query([{"$match": {"domain": "test_domain_2"}},
          {"$group": {"_id": "$my_key", "my_key": {"$sum": 1}}}]).save()

    # get the MongoClient
    client = pymodm.connection._get_db()

    # create document in mycoll
    for my_key in ("2017", "2018", "2019", "2020"):
        client.mycoll.delete_many({"domain": "test_domain_2",
                                             "my_key": my_key})
        client.mycoll.insert_one({"domain": "test_domain_2",
                                            "my_key": my_key})

    client.mycoll.insert_one({"domain": "test_domain_2", "my_key": "2020"})
