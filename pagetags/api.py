from flask_restful import Resource

from pagetags import models, db


class TagsResource(Resource):
    def get(self):
        tags = db.session.query(models.Tag).all()

        return [tag.name for tag in tags]


class TagUrlsResource(Resource):
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
