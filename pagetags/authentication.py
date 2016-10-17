from flask_jwt import _default_jwt_payload_handler

from pagetags.models import User, db


def load_user(user_id):
    return db.session.query(User).get(user_id)


def authenticate(username, password):
    return User.authenticate(username, password)


def identity(payload):
    user_id = payload["identity"]
    jti = payload["jti"]

    return User.authenticate_using_jti(user_id, jti)


def payload_handler(identity):
    payload = _default_jwt_payload_handler(identity)

    payload["jti"] = identity.jti

    return payload
