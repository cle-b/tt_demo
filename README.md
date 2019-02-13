[![Build Status](https://travis-ci.org/cle-b/tt_demo.svg?branch=master)](https://travis-ci.org/cle-b/tt_demo) [![codecov](https://codecov.io/gh/cle-b/tt_demo/branch/master/graph/badge.svg)](https://codecov.io/gh/cle-b/tt_demo)

# tt_demo

This project is my implementation of the Toucan Toco back tech test for technical interview.

## Technical choices and relevant things (in my point of view :) )

I have implemented this REST API using Connexion. [Connexion](https://github.com/zalando/connexion) is a framework that automagically handles HTTP requests based on OpenAPI specification of your API described in YAML format. 

I think there are a lot of good reason to write the spec first. This guarantees that your API will follow the specification that you wrote.

Of course, it's also because OpenAPI allow us to provide a good documentation (its a very important things for me. I lose to much time to implement clients for API with incomplet documentations...).

For the testing part, I use pytest and coverage. Github, Travis-CI and codecov.io for the CI.

About the performance, two points:
  * the queries are stored in a dedicated collection. One document by query. I use the checksum of the description as an index. Therefore, it's really fast to find if a query has already been recorded.

  * i use the bulk_write operation in order to create all the queries for a configuration file in order to avoid to much requests between the app server and the database.

I don't address the authentication point because I haven't implement it. It's not a simple task to do in a short time so I prefer to bypass this point instead of doing a bad work. As this kind of API is probably implemented in a microservice, a JWT bearer token for the authentication can be a good solution.

## Installation

You can install the app using the following command (tested on Ubuntu 18.10):

```bash
# download the project from github
git clone https://github.com/cle-b/tt_demo

# create a python virtual env
cd tt_demo
python3 -m venv venv
source venv/bin/activate

# install the requirements
pip install -r requirements.txt

# launch the mongodb docker given in example
sudo docker pull toucantoco/backtechtest
sudo docker run -d --rm -i -p 27017:27017 toucantoco/backtechtest
# or set the TT_MONGO_URI environment variable
# export TT_MONGO_URI=mongodb://localhost:27017/mytest

# populate the db with examples
python -c 'from populate_db import populate_db; populate_db()'

# install the app
pip install -e .

# enable the debug mode if you want to browse the API documentation from your browser
export FLASK_DEBUG=1

# launch the app
python tt_demo/app.py
```

## Usage

If you have activated the debug mode, the API documentation if available here: http://localhost:9090/ui/.
You can test directly the API from the documenation.

Otherwise it's very simple.

For the queries creation, just post your CSON configuration file to /queries
You can use the file tests/cson/config.test.cson for example (queries used for the tests)
The response contains the same configuration file with ID instead of description for the queries
```bash
curl -X POST "http://localhost:9090/queries" -H  "accept: application/octet-stream" -H  "Content-Type: application/octet-stream" --data-binary @tests/cson/config.test.cson
```

Get the list of all query IDs
```bash
curl -X GET "http://localhost:9090/queries" -H  "accept: application/json"
```

Execute a query on mycoll collection, without filter
```bash
curl -X POST "http://localhost:9090/mycoll/query?id=ef9a570053038ba08b5ca89dac4a3a6c" -H  "accept: */*" -H  "Content-Type: application/json" -d "{}"
```

Execute a query on mycoll collection, with a filter
```bash
curl -X POST "http://localhost:9090/mycoll/query?id=61dbb89ca5de54506143f3a7a07c2763" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"filter\":\"2020\"}"
```

Execute a query of type aggregate on mycoll collection
```bash
curl -X POST "http://localhost:9090/mycoll/query?id=89da2cbd2e566a77b0e96ebf06c26daf" -H  "accept: */*" -H  "Content-Type: application/json" -d "{}"
```
