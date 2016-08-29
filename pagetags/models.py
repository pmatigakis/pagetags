from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from pagetags import db


posting_tags = db.Table(
    "posting_tags",
    db.Column("posting_id", db.Integer, nullable=False),
    db.Column("tag_id", db.Integer, nullable=False),
    db.ForeignKeyConstraint(
        ["posting_id"], ["postings.id"], name="fk_posting_id__postings"),
    db.ForeignKeyConstraint(["tag_id"], ["tags.id"], name="fk_tag_id__tags"),
)


class User(UserMixin, db.Model):
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

    @classmethod
    def authenticate(cls, username, password):
        user = db.session.query(User)\
                         .filter_by(username=username)\
                         .one_or_none()

        if user and check_password_hash(user.password, password):
            return user

        return None


class Tag(db.Model):
    __tablename__ = "tags"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_tags"),
        db.UniqueConstraint("name", name="uq_tags__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    postings = db.relationship(
        'Posting', secondary=posting_tags, back_populates="tags")

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

        return tag

    def get_postings_by_page(self, page, per_page=10):
        return Posting.query\
                      .filter(Posting.tags.contains(self))\
                      .order_by(db.desc(Posting.added_at))\
                      .paginate(page=page, per_page=per_page)

    def get_postings(self):
        return db.session.query(Posting)\
                         .filter(Posting.tags.contains(self))\
                         .all()


class Url(db.Model):
    __tablename__ = "urls"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_urls"),
        db.UniqueConstraint("url", name="uq_urls__url")
    )

    id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    postings = db.relationship("Posting", back_populates="url")

    @classmethod
    def create(cls, url):
        url_object = cls(url=url, added_at=datetime.utcnow())

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

    @classmethod
    def get_or_create(cls, url):
        url_object = cls.get_by_url(url)

        if url_object is None:
            url_object = cls.create(url)

        return url_object

    @classmethod
    def get_postings(cls, url):
        url_object = cls.get_by_url(url)

        return db.session.query(Posting)\
                         .filter(Posting.url == url_object)\
                         .order_by(db.desc(Posting.added_at))\
                         .all()


class Posting(db.Model):
    __tablename__ = "postings"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_postings"),
        db.ForeignKeyConstraint(["url_id"], ["urls.id"],
                                name="fk_url_id__urls")
    )

    id = db.Column(db.Integer, nullable=False)
    url_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    url = db.relationship("Url", back_populates="postings")
    tags = db.relationship(
        'Tag', secondary=posting_tags, back_populates="postings")

    @classmethod
    def create(cls, title, url, tags):
        url_object = Url.get_or_create(url)

        tag_collection = [Tag.get_or_create(tag) for tag in tags]

        posting = cls(
            title=title,
            url=url_object,
            tags=tag_collection,
            added_at=datetime.utcnow()
        )

        db.session.add(posting)

        return posting

    @classmethod
    def get_latest(cls, count=20):
        return db.session.query(cls)\
                         .order_by(db.desc(cls.added_at))\
                         .limit(count)
