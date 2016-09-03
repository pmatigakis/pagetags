# Introduction

Pagetags is a link aggregation Flask application. It was developed so that it
can be used to categorize web pages that will be later used for the creation of
a dataset for machine learning experiments. That is the reason it implements
only the basic functionality required for this task.

# Installation

Create a virtual environment to host the application.

```
virtualenv --python=python2.7 virtualenv

source virtualenv/bin/activate
```

Download the source code and execute the setup script

```
python setup.py install
```

Edit the *alembic.ini* file and set the *sqlalchemy.url* variable to the settings
required by the RDBMS you plan to use. Pagetags has been testen only on SQLite
and Postgresql but it should work on any database supported by SQLAlchemy.
You will have to create the database and a user on your RDBMS.

Run the database migrations

```
alembic upgrade head
```

Create a file named *settings.py* and add the following variables. In this
example the database that will be used is Postgresql.

```python
import logging
DEBUG = False

SECRET_KEY = "add a secret key here"

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://username:password@localhost/pagetags"

LOG_LEVEL = logging.DEBUG
```

# Usage

Create a used with the cli tool

```
pagetags users create --username user1 --password user1password
```

Start the server

```
pagetags runserver
```

Open [http://localhost:5000/login](http://localhost:5000/login) and enter your credentions
in order to login. After that you will be redirected to the main page.

# API

Pagetags has a REST API that can be used to access the saved posts.

## Authentication

All API endpoints require authentication. [JWT](https://jwt.io/) is used as the
authentication mechanism. All requests must contain the following header.

```
Authorization: JWT your.token.here
```


### POST /auth

Create a JWT token

Request Body

```javascript
{
    "username": "user1",
    "password": "user1password"
}
```

Response
```javascript
{
    "access_token": "aaaa.bbb.cccc"
}
```

### GET /api/v1/tags

Returns the saved tags

Response

```javascript
["tag1", "tag2", "tag3"]
```

### Get /api/v1/tag/\<tag\>

Returns the postings for this tag

Response

```javascript
[
    {
        "id": 123,
        "title": "posting title",
        "url": "http://www.example.com/page_1",
        "tags": ["tag1", "tag2"]
    }
]
```

### Get /api/v1/url/url=\<url\>

Returns the postings for this url

Response

```javascript
[
    {
        "id": 123,
        "title": "posting title",
        "url": "http://www.example.com/page_1",
        "tags": ["tag1", "tag2"],
        "added_at": "2016/01/01 16:00:00"
    }
]
```