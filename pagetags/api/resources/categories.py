from flask_restful import Resource, abort, fields, marshal_with
from flask_restful_swagger import swagger
from flask_jwt import jwt_required

from pagetags.models import Category
from pagetags import error_codes
from pagetags import reqparsers
from pagetags.api.models import CategoryPosts


class CategoryPortsResource(Resource):
    @swagger.operation(
        nickname='category_posts',
        notes='Retrieve the category posts',
        parameters=[
            {
                "name": "category",
                "description": "The category to use",
                "required": True,
                "allowMultiple": False,
                "dataType": fields.String.__name__,
                "paramType": "path"
            }
        ],
        responseClass=CategoryPosts.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "retrieved the category posts"
            },
            {
                "code": 404,
                "message": "category doesn't exist"
            }
        ]
    )
    @marshal_with(CategoryPosts.resource_fields)
    @jwt_required()
    def get(self, category):
        category_object = Category.get_by_name(category)

        if category_object is None:
            return abort(
                404,
                error="category doesn't exist",
                category=category,
                error_code=error_codes.CATEGORY_NOT_FOUND
            )

        args = reqparsers.categories_posts.parse_args()

        paginator = category_object.get_posts_by_page(args.page, args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": post.url.url,
                "tags": post.tag_names(),
                "categories": post.category_names(),
                "added_at": post.added_at
            }
            for post in paginator.items
        ]

        return {
            "category_id": category_object.id,
            "category": category_object.name,
            "posts": posts,
            "has_more": paginator.has_next,
            "page": args.page,
            "per_page": args.per_page
        }
