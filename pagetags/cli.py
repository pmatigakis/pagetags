import os

from flask_script import Command, Option
from flask_script import Manager

from pagetags import db
from pagetags.main import create_app
from pagetags.models import User


class InitDB(Command):
    """Initialize the database"""

    def run(self):
        db.create_all()


class CreateUser(Command):
    """Create a new user"""

    option_list = (
        Option('--username', required=True),
        Option('--password', required=True)
    )

    def run(self, username, password):
        User.create(username, password)

        db.session.commit()


class DeleteUser(Command):
    """Delete a user"""

    option_list = (
        Option('--username', required=True),
    )

    def run(self, username):
        User.delete(username)

        db.session.commit()


class ChangeUserPassword(Command):
    """Change a user's password"""

    option_list = (
        Option('--username', required=True),
        Option('--password', required=True)
    )

    def run(self, username, password):
        user = User.get_by_username(username)

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


def main():
    settings_path = os.path.join(os.getcwd(), "settings.py")
    environment_type = os.getenv("PAGETAGS_ENV", "production")

    app = create_app(settings_path, environment_type)

    users_manager = Manager(help="User management commands")
    users_manager.add_command("create", CreateUser())
    users_manager.add_command("delete", DeleteUser())
    users_manager.add_command("change_password", ChangeUserPassword())
    users_manager.add_command("list", ListUsers())

    manager = Manager(app)
    manager.add_command("initdb", InitDB())

    manager.add_command("users", users_manager)

    manager.run()
