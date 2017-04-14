import os

from flask_script import Manager

from pagetags.main import create_app
from pagetags.cli import users, database


def main():
    settings_path = os.path.join(os.getcwd(), "settings.py")
    environment_type = os.getenv("PAGETAGS_ENV", "production")

    app = create_app(settings_path, environment_type)

    users_manager = Manager(help="User management commands")
    users_manager.add_command("create", users.CreateUser())
    users_manager.add_command("delete", users.DeleteUser())
    users_manager.add_command("change_password", users.ChangeUserPassword())
    users_manager.add_command("list", users.ListUsers())

    manager = Manager(app)
    manager.add_command("initdb", database.InitDB())

    manager.add_command("users", users_manager)

    manager.run()
