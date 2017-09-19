from flask_restful import Resource, abort
from flask_jwt import jwt_required
from flask import current_app
from flask_restful_swagger import swagger
from flask_restful import fields, marshal_with

from pagetags import models, db, reqparsers, error_codes
from pagetags.api.models import TagPosts, Tags


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
        tag_object = models.Tag.get_by_name(db.session, tag)

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
