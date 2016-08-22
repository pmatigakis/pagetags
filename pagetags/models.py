from datetime import datetime

from werkzeug.security import generate_password_hash

from pagetags import db


url_tags = db.Table(
    "url_tags",
    db.Column("url_id", db.Integer, nullable=False),
    db.Column("tag_id", db.Integer, nullable=False),
    db.ForeignKeyConstraint(["url_id"], ["urls.id"], name="fk_url_id__urls"),
    db.ForeignKeyConstraint(["tag_id"], ["tags.id"], name="fk_tag_id__tags"),
)


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_users"),
        db.UniqueConstraint("username", name="uq_users__username")
    )

    id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @classmethod
    def create(cls, username, password):
        user = cls(
            username=username,
            password=generate_password_hash(password)
        )

        db.session.add(user)

        return user

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).one_or_none()

    @classmethod
    def delete(cls, username):
        user = cls.get_by_username(username)

        db.session.delete(user)

        return user

    def change_password(self, password):
        self.password = generate_password_hash(password)


class Tag(db.Model):
    __tablename__ = "tags"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_tags"),
        db.UniqueConstraint("name", name="uq_tags__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    urls = db.relationship('Url', secondary=url_tags, back_populates="tags")

    @classmethod
    def get_by_name(cls, name):
        return db.session.query(cls).filter_by(name=name).one_or_none()

    @classmethod
    def create(cls, name):
        tag = cls(name=name)

        db.session.add(tag)

        return tag

    @classmethod
    def get_or_create(cls, name):
        tag = cls.get_by_name(name)

        if tag is None:
            tag = cls.create(name)

            db.session.add(tag)

        return tag


class Url(db.Model):
    __tablename__ = "urls"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_urls"),
        db.UniqueConstraint("url", name="uq_urls__url")
    )

    id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    tags = db.relationship('Tag', secondary=url_tags, back_populates="urls")

    @classmethod
    def create(cls, url, tags):
        url_object = cls(url=url, tags=tags, added_at=datetime.utcnow())

        db.session.add(url_object)

        return url_object

    @classmethod
    def get_by_url(cls, url):
        return db.session.query(cls).filter_by(url=url).one_or_none()

    @classmethod
    def get_latest(cls, count=20):
        return db.session.query(cls)\
                         .order_by(db.desc(cls.added_at))\
                         .limit(count)
