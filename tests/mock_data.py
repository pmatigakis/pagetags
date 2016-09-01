from datetime import datetime

from pagetags.models import Posting, User


def load_users(db):
    User.create("user1", "user1-password")

    db.session.commit()


def load_mock_postings(db):
    posting_1 = Posting.create(
        "page 1",
        "http://www.example.com/page_1",
        ["tag1", "tag2"]
    )

    posting_1.added_at = datetime(2016, 5, 1, 10, 20, 30)

    posting_2 = Posting.create(
        "page 2",
        "http://www.example.com/page_2",
        ["tag1", "tag3"]
    )

    posting_2.added_at = datetime(2016, 5, 1, 11, 20, 30)

    posting_3 = Posting.create(
        "page 3",
        "http://www.example.com/page_1",
        ["tag1", "tag3"]
    )

    posting_3.added_at = datetime(2016, 5, 1, 12, 20, 30)

    db.session.commit()
