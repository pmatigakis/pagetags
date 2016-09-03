from datetime import datetime, timedelta

from pagetags.models import Posting, User


def load_users(db):
    User.create("user1", "user1-password")

    db.session.commit()


def load_mock_postings(db):
    current_time = datetime.utcnow()

    posting_1 = Posting.create(
        "page 1",
        "http://www.example.com/page_1",
        ["tag1", "tag2"]
    )

    posting_1.added_at = current_time - timedelta(hours=5)

    posting_2 = Posting.create(
        "page 2",
        "http://www.example.com/page_2",
        ["tag1", "tag3"]
    )

    posting_2.added_at = current_time - timedelta(hours=4)

    posting_3 = Posting.create(
        "page 3",
        "http://www.example.com/page_1",
        ["tag1", "tag3"]
    )

    posting_3.added_at = current_time - timedelta(hours=3)

    posting_4 = Posting.create(
        "page 4",
        "http://www.example.com/page_4",
        ["tag4", "tag5"]
    )

    posting_4.added_at = current_time - timedelta(hours=2)

    db.session.commit()
