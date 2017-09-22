from flask import current_app, render_template

from pagetags import models, reqparsers
from pagetags.models import db


def tag(name):
    args = reqparsers.tag_posts.parse_args()

    postings_item_count = current_app.config["TAG_POSTS_PER_PAGE"]

    msg = u"listing posts for tag: tag({}) page({})"
    current_app.logger.info(msg.format(name, args.page))

    tag_object = models.Tag.get_by_name(db.session, name)

    if tag_object is None:
        current_app.logger.warning(u"tag doesn't exist: tag({})".format(name))
        return render_template("404.html"), 404

    paginator = tag_object.get_posts_by_page(
        args.page, per_page=postings_item_count)

    return render_template("tag.html", tag=tag_object, paginator=paginator)
