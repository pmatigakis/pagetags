from pagetags import db
from pagetags.models import User


def load_user(user_id):
    return db.session.query(User).get(user_id)
