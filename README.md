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

You will need a Postgresql database and the user credentials for that database.
Edit the *alembic.ini* file and set the *sqlalchemy.url* variable to the required
settings for your database.

Run the database migrations

```
alembic upgrade head
```

Create a file named *settings.py* and add the following variables.

```python
import logging
DEBUG = False

SECRET_KEY = "add a secret key here"

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://username:password@localhost/pagetags"

LOG_LEVEL = logging.DEBUG
```

# Usage

Create a user with the cli tool

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

### Get /api/v1/tag/\<tag\>[?page=\<page\>]

Returns the posts for this tag

Response

```javascript
{
    "has_more": false,
    "page": 1,
    "per_page": 10,
    "posts": [
        {
            "id": 123,
            "title": "post title",
            "url": "http://www.example.com/page_1",
            "tags": ["tag1", "tag2"],
            "added_at": "2016/03/21 12:20:00"
        },
        {
            "id": 122,
            "title": "post title",
            "url": "http://www.example.com/page_2",
            "tags": ["tag1", "tag3"],
            "added_at": "2016/03/21 11:00:00"
        },
    ] 
}
```

### Get /api/v1/url/url=\<url\>[?page=\<page\>]

Returns the posts for this url

Response

```javascript
{
    "has_more": false,
    "page": 1,
    "per_page": 10,
    "posts": [
        {
            "id": 123,
            "title": "post title",
            "url": "http://www.example.com/page_1",
            "tags": ["tag1", "tag2"],
            "added_at": "2016/03/21 12:20:00"
        },
        {
            "id": 122,
            "title": "post title",
            "url": "http://www.example.com/page_2",
            "tags": ["tag1", "tag3"],
            "added_at": "2016/03/21 11:00:00"
        },
    ] 
}
```

### POST /api/v1/posts

Add a new post

Request body

```javascript
{
    "title": "page title",
    "url": "http://www.example.com/page_1",
    "tags": ["tag1", "tag2"]
}
```

Response

```javascript
{
    "id": 123
}
```

### GET /api/v1/posts[?page=\<page\>]

Get the latest posts

Response

```javascript
{
    "has_more": false,
    "page": 1,
    "per_page": 10,
    "posts": [
        {
            "id": 123,
            "title": "post title",
            "url": "http://www.example.com/page_1",
            "tags": ["tag1", "tag2"],
            "added_at": "2016/03/21 12:20:00"
        },
        {
            "id": 122,
            "title": "post title",
            "url": "http://www.example.com/page_2",
            "tags": ["tag1", "tag3"],
            "added_at": "2016/03/21 11:00:00"
        },
    ] 
}
```
