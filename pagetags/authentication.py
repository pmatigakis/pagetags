from pagetags.models import User, db


def load_user(user_id):
    return db.session.query(User).get(user_id)


def authenticate(username, password):
    return User.authenticate(username, password)


def identity(payload):
    user_id = payload["identity"]

    return db.session.query(User).get(user_id)
