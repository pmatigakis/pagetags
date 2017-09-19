from flask_script import Command, Option

from pagetags import db
from pagetags.models import User


class CreateUser(Command):
    """Create a new user"""

    option_list = (
        Option('--username', required=True),
        Option('--password', required=True)
    )

    def run(self, username, password):
        User.create(db.session, username, password)

        db.session.commit()


class DeleteUser(Command):
    """Delete a user"""

    option_list = (
        Option('--username', required=True),
    )

    def run(self, username):
        User.delete(db.session, username)

        db.session.commit()


class ChangeUserPassword(Command):
    """Change a user's password"""

    option_list = (
        Option('--username', required=True),
        Option('--password', required=True)
    )

    def run(self, username, password):
        user = User.get_by_username(db.session, username)

        if user is None:
            print("Failed to change user pasword")
            return

        user.change_password(password)

        db.session.commit()


class ListUsers(Command):
    """List the registered users"""

    def run(self):
        for user in db.session.query(User).all():
            print("{}\t{}".format(user.id, user.username))
