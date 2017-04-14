from flask_script import Command, Option
from flask import current_app

from pagetags.models import User
from pagetags.authentication import create_token


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

        token = create_token(user.id, user.jti, secret, algorithm, expires_at)

        print(token)
