from flask_script import Command

from pagetags import db


class InitDB(Command):
    """Initialize the database"""

    def run(self):
        db.create_all()
