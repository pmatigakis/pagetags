from flask_restful import Resource, abort
from flask_jwt import jwt_required
from flask import current_app
from flask_restful_swagger import swagger
from flask_restful import fields, marshal_with

from pagetags import models, reqparsers, error_codes
from pagetags.api.models import URLPosts


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
