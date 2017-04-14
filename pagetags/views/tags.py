from flask_login import login_required
from flask import current_app, render_template

from pagetags import models, reqparsers


@login_required
def tag(name):
    args = reqparsers.tag_posts.parse_args()

    postings_item_count = current_app.config["TAG_POSTS_PER_PAGE"]

    msg = u"listing posts for tag: tag({}) page({})"
    current_app.logger.info(msg.format(name, args.page))

    tag_object = models.Tag.get_by_name(name)

    if tag_object is None:
        current_app.logger.warning(u"tag doesn't exist: tag({})".format(name))
        return render_template("404.html"), 404

    paginator = tag_object.get_posts_by_page(
        args.page, per_page=postings_item_count)

    return render_template("tag.html", tag=tag_object, paginator=paginator)


@login_required
def tags():
    args = reqparsers.tags_posts.parse_args()

    tags_item_count = current_app.config["TAGS_PER_PAGE"]

    msg = u"listing tags: page({}), per_page({})"
    current_app.logger.info(msg.format(args.page, tags_item_count))

    paginator = models.Tag.get_tags_by_page(args.page, tags_item_count)

    return render_template("tags.html", paginator=paginator)
