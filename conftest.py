import pytest

import tt_demo

mongdb_uri = "mongodb://localhost:27017/mytest"

app = tt_demo.create_app("tt_demo",
                         mongodb_uri=mongdb_uri,
                         port=9090,
                         debug=False)


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c
