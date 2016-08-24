from flask_restful import Resource
from flask_jwt import jwt_required

from pagetags import models, db


class TagsResource(Resource):
    @jwt_required()
    def get(self):
        tags = db.session.query(models.Tag).all()

        return [tag.name for tag in tags]


class TagUrlsResource(Resource):
    @jwt_required()
    def get(self, tag):
        tag = models.Tag.get_by_name(tag)

        urls = tag.get_urls()

        return [
            {
                "id": url.id,
                "title": url.title,
                "url": url.url
            }
            for url in urls
        ]
