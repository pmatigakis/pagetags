from datetime import datetime
from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates

from pagetags import db


post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, nullable=False),
    db.Column("tag_id", db.Integer, nullable=False),
    db.ForeignKeyConstraint(
        ["post_id"], ["posts.id"],
        name="fk_post_id__posts",
        ondelete="CASCADE",
        onupdate="CASCADE"
    ),
    db.ForeignKeyConstraint(
        ["tag_id"], ["tags.id"],
        name="fk_tag_id__tags",
        ondelete="CASCADE",
        onupdate="CASCADE"
    )
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
    jti = db.Column(db.String(32), nullable=False)

    @classmethod
    def create(cls, session, username, password):
        user = cls(
            username=username,
            password=generate_password_hash(password),
            jti=uuid4().hex
        )

        session.add(user)

        return user

    @classmethod
    def get_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).one_or_none()

    @classmethod
    def delete(cls, session, username):
        user = cls.get_by_username(session, username)

        session.delete(user)

        return user

    def change_password(self, password):
        self.password = generate_password_hash(password)
        self.jti = uuid4().hex

    @classmethod
    def authenticate(cls, session, username, password):
        user = session.query(User)\
                      .filter_by(username=username)\
                      .one_or_none()

        if user and check_password_hash(user.password, password):
            return user

        return None

    @classmethod
    def authenticate_using_jti(cls, session, user_id, jti):
        return session.query(User)\
                      .filter_by(id=user_id, jti=jti)\
                      .one_or_none()

    def __unicode__(self):
        return self.username


class Tag(db.Model):
    __tablename__ = "tags"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_tags"),
        db.UniqueConstraint("name", name="uq_tags__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    posts = db.relationship(
        'Post',
        secondary=post_tags,
        back_populates="tags"
    )

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).one_or_none()

    @classmethod
    def create(cls, session, name):
        tag = cls(name=name)

        session.add(tag)

        return tag

    @classmethod
    def get_or_create(cls, session, name):
        tag = cls.get_by_name(session, name)

        if tag is None:
            tag = cls.create(session, name)

        return tag

    @classmethod
    def get_tags_by_page(cls, page, per_page=10):
        # TODO: pass the session as argument

        return cls.query\
                  .order_by(db.asc(cls.name))\
                  .paginate(page=page, per_page=per_page)

    def get_posts_by_page(self, page, per_page=10):
        return Post.query\
                   .filter(Post.tags.contains(self))\
                   .order_by(db.desc(Post.added_at))\
                   .paginate(page=page, per_page=per_page, error_out=False)

    def get_posts(self, session):
        return session.query(Post)\
                      .filter(Post.tags.contains(self))\
                      .all()

    def post_count(self, session, ):
        return session.query(Post) \
                      .filter(Post.tags.contains(self)) \
                      .count()

    def __unicode__(self):
        return self.name


class Url(db.Model):
    __tablename__ = "urls"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_urls"),
        db.UniqueConstraint("url", name="uq_urls__url")
    )

    URL_LENGTH = 1024

    id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(URL_LENGTH), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship(
        "Post",
        back_populates="url",
        cascade="all, delete-orphan"
    )

    @classmethod
    def create(cls, session, url):
        url_object = cls(url=url, added_at=datetime.utcnow())

        session.add(url_object)

        return url_object

    @classmethod
    def get_by_url(cls, session, url):
        return session.query(cls).filter_by(url=url).one_or_none()

    @classmethod
    def get_latest(cls, session, count=20):
        return session.query(cls)\
                      .order_by(db.desc(cls.added_at))\
                      .limit(count)

    @classmethod
    def get_or_create(cls, session, url):
        url_object = cls.get_by_url(session, url)

        if url_object is None:
            url_object = cls.create(session, url)

        return url_object

    @classmethod
    def get_posts(cls, session, url):
        url_object = cls.get_by_url(session, url)

        return session.query(Post)\
                      .filter(Post.url == url_object)\
                      .order_by(db.desc(Post.added_at))\
                      .all()

    def get_posts_by_page(self, page, per_page=10):
        # TODO: pass the session as argument

        return Post.query\
                   .filter(Post.url == self)\
                   .order_by(db.desc(Post.added_at))\
                   .paginate(page=page, per_page=per_page, error_out=False)

    @validates("url")
    def validate_url(self, key, url):
        if len(url) == 0 or len(url) > self.URL_LENGTH:
            raise ValueError()

        return url

    def __unicode__(self):
        return self.url


class Post(db.Model):
    __tablename__ = "posts"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_posts"),
        db.ForeignKeyConstraint(
            ["url_id"], ["urls.id"],
            name="fk_url_id__urls",
            ondelete="CASCADE",
            onupdate="CASCADE"
        )
    )

    TITLE_LENGTH = 256

    id = db.Column(db.Integer, nullable=False)
    url_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(TITLE_LENGTH), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    url = db.relationship(
        "Url",
        back_populates="posts"
    )

    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        back_populates="posts"
    )

    categories = db.relationship(
        "Category",
        secondary="post_categories"
    )

    @classmethod
    def create(cls, session, title, url, tags, categories):
        url_object = Url.get_or_create(session, url)

        tag_collection = [Tag.get_or_create(session, tag) for tag in tags]
        category_collection = [
            Category.get_or_create(session, category)
            for category in categories
        ]

        post = cls(
            title=title,
            url=url_object,
            tags=tag_collection,
            added_at=datetime.utcnow(),
            categories=category_collection
        )

        session.add(post)

        return post

    @classmethod
    def get_latest(cls, session, count=20):
        return session.query(cls)\
                      .order_by(db.desc(cls.added_at))\
                      .limit(count)

    def tag_names(self):
        tags = [tag.name for tag in self.tags]

        return sorted(tags)

    def category_names(self):
        categories = [category.name for category in self.categories]

        return sorted(categories)

    @classmethod
    def get_latest_by_page(cls, page, per_page=10):
        # TODO: pass the session as argument

        return cls.query\
                  .order_by(db.desc(cls.added_at))\
                  .paginate(page=page, per_page=per_page)

    @classmethod
    def get_by_id(cls, session, post_id):
        return session.query(cls).get(post_id)

    @validates("title")
    def validate_title(self, key, title):
        if len(title) == 0 or len(title) > self.TITLE_LENGTH:
            raise ValueError()

        return title

    def update(self, session, title, url, tags):
        self.title = title

        url_object = Url.get_or_create(session, url)

        self.url = url_object

        tag_collection = [Tag.get_or_create(session, tag) for tag in tags]

        self.tags = tag_collection

    def __unicode__(self):
        return self.title


class Category(db.Model):
    __tablename__ = "categories"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_categories"),
        db.UniqueConstraint("name", name="uq_categories__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship(
        "Post",
        secondary="post_categories"
    )

    @classmethod
    def create(cls, session, name):
        category = cls(
            name=name,
            added_at=datetime.now()
        )

        session.add(category)

        return category

    @classmethod
    def get_or_create(cls, session, name):
        category = session.query(cls).filter_by(name=name).one_or_none()

        if category is None:
            category = cls.create(session, name)

        return category

    @classmethod
    def get_by_page(cls, page_num, per_page=10):
        # TODO: pass the session as argument
        return cls.query \
                  .order_by(db.desc(cls.name)) \
                  .paginate(page=page_num, per_page=per_page)

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).one_or_none()

    @classmethod
    def all(cls, session):
        return session.query(cls).order_by(cls.name).all()

    def get_posts_by_page(self, page, per_page=10):
        # TODO: pass the session as argument

        return Post.query\
                   .filter(Post.categories.contains(self))\
                   .order_by(db.desc(Post.added_at))\
                   .paginate(page=page, per_page=per_page, error_out=False)

    def __unicode__(self):
        return self.name


class PostCategory(db.Model):
    __tablename__ = "post_categories"

    __table_args__ = (
        db.PrimaryKeyConstraint(
            "post_id", "category_id",
            name="pk_post_categories"
        ),
        db.ForeignKeyConstraint(
            ["post_id"], ["posts.id"],
            name="fk_post_categories__post_id__posts",
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        db.ForeignKeyConstraint(
            ["category_id"], ["categories.id"],
            name="fk_post_categories__category_id__categories",
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
    )

    post_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    assigned_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    post = db.relationship(
        "Post",
        backref=db.backref("post_categories", cascade="all, delete-orphan")
    )

    category = db.relationship(
        "Category",
        backref=db.backref("post_categories", cascade="all, delete-orphan")
    )

    @classmethod
    def create(cls, session, post, category):
        post_category = cls(
            post=post,
            category=category
        )

        session.add(post_category)

        return post_category
