from flask_script import Command
from flask_script import Manager

from pagetags import db
from pagetags.main import create_app


class InitDB(Command):
    """Initialize the database"""

    def run(self):
        db.create_all()


def main():
    app = create_app()

    manager = Manager(app)
    manager.add_command("initdb", InitDB())

    manager.run()
