from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class Post(object):
    required = ["id", "title", "url", "added_at", "tags", "categories"]
    resource_fields = {
        "id": fields.Integer,
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String),
        "categories": fields.List(fields.String),
        "added_at": fields.DateTime
    }


@swagger.model
@swagger.nested(posts=Post.__name__)
class TagPosts(object):
    required = ["tag_id", "posts", "has_more", "page", "per_page"]
    resource_fields = {
        "tag_id": fields.Integer,
        "posts": fields.List(fields.Nested(Post.resource_fields)),
        "has_more": fields.Boolean,
        "page": fields.Integer,
        "per_page": fields.Integer
    }


@swagger.model
class NewPost(object):
    required = ["title", "url", "tags", "categories"]
    resource_fields = {
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String),
        "categories": fields.List(fields.String)
    }


@swagger.model
class CreatedPost(object):
    required = ["id"]
    resource_fields = {
        "id": fields.Integer
    }


@swagger.model
@swagger.nested(posts=Post.__name__)
class Posts(object):
    required = ["posts", "has_more", "page", "per_page"]
    resource_fields = {
        "posts": fields.List(fields.Nested(Post.resource_fields)),
        "has_more": fields.Boolean,
        "page": fields.Integer,
        "per_page": fields.Integer
    }


@swagger.model
@swagger.nested(posts=Post.__name__)
class URLPosts(object):
    required = ["url_id", "posts", "has_more", "page", "per_page"]
    resource_fields = {
        "url_id": fields.Integer,
        "posts": fields.List(fields.Nested(Post.resource_fields)),
        "has_more": fields.Boolean,
        "page": fields.Integer,
        "per_page": fields.Integer
    }


@swagger.model
class UpdatePost(object):
    required = ["title", "url", "tags"]
    resource_fields = {
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String)
    }


@swagger.model
class UpdatedPost(object):
    required = ["id", "title", "urls", "tags", "added_at", "categories"]
    resource_fields = {
        "id": fields.Integer,
        "title": fields.String,
        "url": fields.String,
        "tags": fields.List(fields.String),
        "categories": fields.List(fields.String),
        "added_at": fields.DateTime
    }


@swagger.model
class Tags(object):
    required = ["tags"]
    resource_fields = {
        "tags": fields.List(fields.String)
    }
