from flask_restful import Resource, abort
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from pagetags import models, db, reqparsers


class TagsResource(Resource):
    @jwt_required()
    def get(self):
        tags = db.session.query(models.Tag).all()

        return [tag.name for tag in tags]


class TagPostingsResource(Resource):
    @jwt_required()
    def get(self, tag):
        tag = models.Tag.get_by_name(tag)

        postings = tag.get_postings()

        return [
            {
                "id": posting.id,
                "title": posting.title,
                "url": posting.url.url,
                "tags": posting.tag_names()
            }
            for posting in postings
        ]


class PostingsResource(Resource):
    @jwt_required()
    def post(self):
        args = reqparsers.posting.parse_args()

        posting = models.Posting.create(args.title, args.url, args.tags)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            abort(500)

        return {"id": posting.id}


class UrlResource(Resource):
    @jwt_required()
    def get(self):
        args = reqparsers.url_query.parse_args()

        return [
            {
                "title": posting.title,
                "url": args.url,
                "tags": posting.tag_names(),
                "added_at": posting.added_at.strftime("%Y/%m/%d %H:%M:%S")
            }
            for posting in models.Url.get_postings(args.url)
        ]
