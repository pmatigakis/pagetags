from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class Post(object):
    resource_fields = {
        "id": fields.Integer,
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String),
        "added_at": fields.DateTime
    }


@swagger.model
@swagger.nested(posts=Post.__name__)
class TagPosts(object):
    resource_fields = {
        "tag_id": fields.Integer,
        "posts": fields.List(fields.Nested(Post.resource_fields)),
        "has_more": fields.Boolean,
        "page": fields.Integer,
        "per_page": fields.Integer
    }


@swagger.model
class NewPost(object):
    resource_fields = {
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String)
    }


@swagger.model
class CreatedPost(object):
    resource_fields = {
        "id": fields.Integer
    }


@swagger.model
@swagger.nested(posts=Post.__name__)
class Posts(object):
    resource_fields = {
        "posts": fields.List(fields.Nested(Post.resource_fields)),
        "has_more": fields.Boolean,
        "page": fields.Integer,
        "per_page": fields.Integer
    }


@swagger.model
class UpdatePost(object):
    resource_fields = {
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String)
    }


@swagger.model
class UpdatedPost(object):
    resource_fields = {
        "id": fields.Integer,
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String),
        "added_at": fields.DateTime
    }
