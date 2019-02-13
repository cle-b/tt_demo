# -*- coding: utf-8 -*
import pytest

from populate_db import populate_db
import tt_demo
from tt_demo.queries import Query

# populate the database with examples for tests
populate_db()

# start the app
mongodb_uri = "mongodb://localhost:27017/mytest"

app = tt_demo.create_app("tt_demo",
                         mongodb_uri=mongodb_uri,
                         port=9090,
                         debug=False)


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c
