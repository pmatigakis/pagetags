from flask_restful import Resource
from flask_jwt import jwt_required

from pagetags import models, db


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
                "url": posting.url.url
            }
            for posting in postings
        ]
