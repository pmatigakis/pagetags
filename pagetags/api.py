from flask_restful import Resource, abort
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app

from pagetags import models, db, reqparsers, error_codes


class TagsResource(Resource):
    @jwt_required()
    def get(self):
        msg = "retrieving available tags"
        current_app.logger.info(msg)

        tags = db.session.query(models.Tag).all()

        return [tag.name for tag in tags]


class TagPostsResource(Resource):
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
                "added_at": post.added_at.strftime("%Y/%m/%d %H:%M:%S")
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
    @jwt_required()
    def post(self):
        args = reqparsers.post.parse_args()

        msg = "adding post: title(%s) url(%s) tags(%s)"
        current_app.logger.info(msg, args.title, args.url, ",".join(args.tags))

        post = models.Post.create(args.title, args.url, args.tags)

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
                "added_at": post.added_at.strftime("%Y/%m/%d %H:%M:%S")
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
            "added_at": post.added_at.isoformat(sep=" "),
            "tags": sorted([tag.name for tag in post.tags])
        }

    @jwt_required()
    def put(self, post_id):
        args = reqparsers.post.parse_args()

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
            "added_at": post.added_at.isoformat(sep=" "),
            "tags": sorted([tag.name for tag in post.tags])
        }
