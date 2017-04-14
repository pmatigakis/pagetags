from flask_jwt import _default_jwt_payload_handler, _default_request_handler
import arrow
import jwt
from flask import request

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


def create_token_payload(user_id, jti, expires_at=None):
    issued_at = arrow.utcnow().timestamp
    not_before = issued_at

    payload = {
        "identity": user_id,
        "iat": issued_at,
        "nbf": not_before,
        "jti": jti
    }

    if expires_at is not None:
        exp = arrow.get(expires_at, "YYYY/MM/DD HH:mm:ss")

        payload["exp"] = exp.timestamp

    return payload


def create_token(user_id, jti, secret, algorithm, expires_at=None):
    payload = create_token_payload(user_id, jti, expires_at)

    return jwt.encode(payload, secret, algorithm)


def request_handler():
    token = request.args.get("api_key")

    return token or _default_request_handler()
