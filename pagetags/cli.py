import os

from flask_script import Command
from flask_script import Manager

from pagetags import db
from pagetags.main import create_app


class InitDB(Command):
    """Initialize the database"""

    def run(self):
        db.create_all()


def main():
    settings_path = os.path.join(os.getcwd(), "settings.py")
    environment_type = os.getenv("PAGETAGS_ENV", "production")

    app = create_app(settings_path, environment_type)

    manager = Manager(app)
    manager.add_command("initdb", InitDB())

    manager.run()
