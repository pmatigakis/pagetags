import os

SECRET_KEY = "testing"

db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test_pagetags.db")

SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % db_path

FRONT_PAGE_ITEM_COUNT = 3
TAG_POSTINGS_PER_PAGE = 2
