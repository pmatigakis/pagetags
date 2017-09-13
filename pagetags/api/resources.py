from flask_restful import Resource, abort
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from flask_restful_swagger import swagger
from flask_restful import fields, marshal_with

from pagetags import models, db, reqparsers, error_codes
from pagetags.api.models import (TagPosts, NewPost, CreatedPost, Posts, Post,
                                 UpdatePost, UpdatedPost, URLPosts, Tags)


class TagsResource(Resource):
    """Tags"""

    @swagger.operation(
        nickname='tags',
        notes='Retrieve the available tags',
        responseClass=Tags.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "retrieved the available tags"
            }
        ]
    )
    @marshal_with(Tags.resource_fields)
    @jwt_required()
    def get(self):
        msg = "retrieving available tags"
        current_app.logger.info(msg)

        tags = db.session.query(models.Tag).all()

        return {
            "tags": [tag.name for tag in tags]
        }


class TagPostsResource(Resource):
    """Tag posts"""

    @swagger.operation(
        nickname='tag_posts',
        notes='Retrieve the tag posts',
        parameters=[
            {
                "name": "tag",
                "description": "The tag to use",
                "required": True,
                "allowMultiple": False,
                "dataType": fields.String.__name__,
                "paramType": "path"
            }
        ],
        responseClass=TagPosts.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "retrieved the tag posts"
            },
            {
                "code": 404,
                "message": "tag doesn't exist"
            }
        ]
    )
    @marshal_with(TagPosts.resource_fields)
    @jwt_required()
    def get(self, tag):
        tag_object = models.Tag.get_by_name(tag)

        if tag_object is None:
            msg = "tag doesn't exist: tag(%s)"
            current_app.logger.warning(msg, tag)

            abort(
                404,
                error="tag doesn't exist",
                tag=tag,
                error_code=error_codes.TAG_NOT_FOUND
            )

        args = reqparsers.tag_posts.parse_args()

        msg = "retrieving posts for tag: tag(%s) page(%d) per_page(%d)"
        current_app.logger.info(msg, tag, args.page, args.per_page)

        paginator = tag_object.get_posts_by_page(args.page, args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": post.url.url,
                "tags": post.tag_names(),
                "added_at": post.added_at
            }
            for post in paginator.items
        ]

        return {
            "tag_id": tag_object.id,
            "posts": posts,
            "has_more": paginator.has_next,
            "page": args.page,
            "per_page": args.per_page
        }


class PostsResource(Resource):
    """Posts"""

    @swagger.operation(
        nickname='create_post',
        notes='Create a post',
        responseClass=CreatedPost.__name__,
        parameters=[
            {
                "name": "body",
                "description": "The new post",
                "required": True,
                "allowMultiple": False,
                "dataType": NewPost.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "created the new post"
            }
        ]
    )
    @marshal_with(CreatedPost.resource_fields)
    @jwt_required()
    def post(self):
        args = reqparsers.post.parse_args()

        msg = "adding post: title(%s) url(%s) tags(%s)"
        current_app.logger.info(msg, args.title, args.url, ",".join(args.tags))

        # TODo: set the post categories
        post = models.Post.create(
            args.title, args.url, args.tags, args.categories)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            msg = "failed to add post: title(%s) url(%s) tags(%s)"
            current_app.logger.exception(
                msg, args.title, args.url, ",".join(args.tags))

            abort(
                500,
                error="failed to add post",
                url=args.url,
                title=args.title,
                tags=args.tags,
                error_code=error_codes.POST_CREATION_DATABASE_ERROR
            )

        return {"id": post.id}

    @swagger.operation(
        nickname='posts',
        notes='Get the posts',
        responseClass=Posts.__name__,
        parameters=[
            {
                "name": "page",
                "description": "The page to retrieve",
                "required": False,
                "allowMultiple": False,
                "dataType": fields.Integer.__name__,
                "paramType": "query"
            },
            {
                "name": "per_page",
                "description": "The posts per page",
                "required": False,
                "allowMultiple": False,
                "dataType": fields.Integer.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Retrieved the posts"
            }
        ]
    )
    @jwt_required()
    def get(self):
        args = reqparsers.posts.parse_args()

        msg = "retrieving posts: page(%d) per_page(%d)"
        current_app.logger.info(msg, args.page, args.per_page)

        paginator = models.Post.get_latest_by_page(
            args.page, per_page=args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": post.url.url,
                "tags": [tag.name for tag in post.tags],
                "added_at": post.added_at.strftime("%Y/%m/%d %H:%M:%S")
            }
            for post in paginator.items
        ]

        return {
            "posts": posts,
            "has_more": paginator.has_next,
            "page": args.page,
            "per_page": args.per_page
        }


class UrlResource(Resource):
    """Urls"""

    @swagger.operation(
        nickname='url_posts',
        notes='Get the posts for a url',
        responseClass=URLPosts.__name__,
        parameters=[
            {
                "name": "url",
                "description": "The url for which to retrieve the posts",
                "required": True,
                "allowMultiple": False,
                "dataType": fields.String.__name__,
                "paramType": "query"
            },
            {
                "name": "page",
                "description": "The page to retrieve",
                "required": False,
                "allowMultiple": False,
                "dataType": fields.Integer.__name__,
                "paramType": "query"
            },
            {
                "name": "per_page",
                "description": "The posts per page",
                "required": False,
                "allowMultiple": False,
                "dataType": fields.Integer.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Retrieved the posts"
            },
            {
                "code": 404,
                "message": "Url doesn't exist"
            }
        ]
    )
    @marshal_with(URLPosts.resource_fields)
    @jwt_required()
    def get(self):
        args = reqparsers.url_query.parse_args()

        msg = "retrieving posts for url: url(%s) page(%d) per_page(%d)"
        current_app.logger.info(msg, args.url, args.page, args.per_page)

        url = models.Url.get_by_url(args.url)

        if url is None:
            msg = "url doesn't exist: url(%s)"
            current_app.logger.warning(msg, args.url)
            abort(
                404,
                error="url doesn't exist",
                url=args.url,
                error_code=error_codes.URL_DOES_NOT_EXIST
            )

        paginator = url.get_posts_by_page(args.page, args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": args.url,
                "tags": post.tag_names(),
                "added_at": post.added_at
            }
            for post in paginator.items
        ]

        return {
            "url_id": url.id,
            "posts": posts,
            "has_more": paginator.has_next,
            "page": args.page,
            "per_page": args.per_page
        }


class PostResource(Resource):
    """Post"""

    @swagger.operation(
        nickname='post',
        notes='Get the post with the given id',
        responseClass=Post.__name__,
        parameters=[
            {
                "name": "post_id",
                "description": "The post id",
                "required": True,
                "allowMultiple": False,
                "dataType": fields.Integer.__name__,
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Retrieved the post"
            },
            {
                "code": 404,
                "message": "The post doesn't exist"
            }
        ]
    )
    @marshal_with(Post.resource_fields)
    @jwt_required()
    def get(self, post_id):
        current_app.logger.info("retrieving post: post_id(%d)", post_id)

        post = models.Post.get_by_id(post_id)

        if post is None:
            msg = "post doesn't exist: post_id(%d)"
            current_app.logger.warning(msg, post_id)

            abort(
                404,
                error="post doesn't exist",
                post_id=post_id,
                error_code=error_codes.POST_DOES_NOT_EXIST
            )

        return {
            "id": post.id,
            "url": post.url.url,
            "title": post.title,
            "added_at": post.added_at,
            "tags": sorted([tag.name for tag in post.tags]),
            "categories":
                sorted([category.name for category in post.categories])
        }

    @swagger.operation(
        nickname='update_post',
        notes='Update the post with the given id',
        responseClass=UpdatedPost.__name__,
        parameters=[
            {
                "name": "body",
                "description": "The post contents",
                "required": True,
                "allowMultiple": False,
                "dataType": UpdatePost.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Updated the post"
            },
            {
                "code": 404,
                "message": "The post doesn't exist"
            }
        ]
    )
    @marshal_with(UpdatedPost.resource_fields)
    @jwt_required()
    def put(self, post_id):
        args = reqparsers.update_post.parse_args()

        msg = "updating post: post_id(%d) title(%s) url(%s) tags(%s)"
        current_app.logger.info(
            msg, post_id, args.title, args.url, ",".join(args.tags))

        post = models.Post.get_by_id(post_id)

        if post is None:
            msg = "post doesn't exist: post_id(%d)"
            current_app.logger.warning(msg, post_id)

            abort(
                404,
                error="post doesn't exist",
                post_id=post_id,
                error_code=error_codes.POST_DOES_NOT_EXIST
            )

        post.update(args.title, args.url, args.tags)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            msg = "failed to update post: post_id(%d)"
            current_app.logger.exception(msg, post_id)

            abort(
                404,
                error="failed to update post",
                post_id=post_id,
                error_code=error_codes.POST_UPDATE_DATABASE_ERROR
            )

        return {
            "id": post.id,
            "url": post.url.url,
            "title": post.title,
            "added_at": post.added_at,
            "tags": sorted([tag.name for tag in post.tags]),
            "categories":
                sorted([category.name for category in post.categories])
        }
