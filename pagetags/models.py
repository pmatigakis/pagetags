from pagetags import db


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_users"),
        db.UniqueConstraint("username", name="uq_users__username")
    )

    id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Tag(db.Model):
    __tablename__ = "tags"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_tags"),
        db.UniqueConstraint("name", name="uq_tags__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)


class Domain(db.Model):
    __tablename__ = "domains"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_domains"),
        db.UniqueConstraint("name", name="uq_domains__name")
    )

    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)


class Url(db.Model):
    __tablename__ = "urls"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_urls"),
        db.ForeignKeyConstraint(["domain_id"],
                                ["domains.id"],
                                name="fk_urls__domain_id__domains"),
        db.UniqueConstraint("url", name="uq_urls__url")
    )

    id = db.Column(db.Integer, nullable=False)
    domain_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(1024), nullable=False)
