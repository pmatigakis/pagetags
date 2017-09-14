from flask import current_app, render_template

from pagetags import models, reqparsers


def index():
    front_page_item_count = current_app.config["FRONT_PAGE_ITEM_COUNT"]

    args = reqparsers.posts.parse_args()

    msg = u"listing posts: page(%d) items_in_page(%d)"
    current_app.logger.info(msg, args.page, front_page_item_count)

    paginator = models.Post.get_latest_by_page(
        page=args.page, per_page=front_page_item_count)

    return render_template("index.html", paginator=paginator)
