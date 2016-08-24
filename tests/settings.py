import os

SECRET_KEY = "testing"

db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test_pagetags.db")

SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % db_path
