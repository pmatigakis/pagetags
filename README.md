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

# Documentation

Use Sphinx to build the documentation

```
cd docs
make html
```

# API

Pagetags has a REST api that can be used to add and retrieve posts. More
details can be found in the `Pagetags API` section of the documentation.

A Swagger documentation page is also available at `/api/spec.html`
