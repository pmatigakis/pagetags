from flask_script import Command, Option
from flask import current_app
import jwt

from pagetags.models import User
from pagetags.authentication import create_token_payload


class CreateToken(Command):
    """Create a token"""

    option_list = [
        Option("--username", required=True),
        Option("--expires_at")
    ]

    def run(self, username, expires_at):
        secret = current_app.config['JWT_SECRET_KEY']
        algorithm = current_app.config['JWT_ALGORITHM']

        user = User.get_by_username(username)
        if user is None:
            print("Unknown user {}".format(username))
            return

        payload = create_token_payload(user.id, user.jti, expires_at)

        token = jwt.encode(payload, secret, algorithm)

        print(token)
