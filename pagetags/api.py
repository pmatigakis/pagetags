from flask_restful import Resource, abort
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from pagetags import models, db, reqparsers


class TagsResource(Resource):
    @jwt_required()
    def get(self):
        tags = db.session.query(models.Tag).all()

        return [tag.name for tag in tags]


class TagPostsResource(Resource):
    @jwt_required()
    def get(self, tag):
        tag = models.Tag.get_by_name(tag)

        args = reqparsers.tag_posts.parse_args()

        paginator = tag.get_posts_by_page(args.page, args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": post.url.url,
                "tags": post.tag_names(),
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


class PostsResource(Resource):
    @jwt_required()
    def post(self):
        args = reqparsers.post.parse_args()

        post = models.Post.create(args.title, args.url, args.tags)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            abort(500)

        return {"id": post.id}

    @jwt_required()
    def get(self):
        args = reqparsers.posts.parse_args()

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
    @jwt_required()
    def get(self):
        args = reqparsers.url_query.parse_args()

        url = models.Url.get_by_url(args.url)

        paginator = url.get_posts_by_page(args.page, args.per_page)

        posts = [
            {
                "id": post.id,
                "title": post.title,
                "url": args.url,
                "tags": post.tag_names(),
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
