from flask_login import login_required
from flask import current_app, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from pagetags import forms, db, models, reqparsers


@login_required
def index():
    front_page_item_count = current_app.config["FRONT_PAGE_ITEM_COUNT"]

    args = reqparsers.posts.parse_args()

    msg = u"listing posts: page(%d) items_in_page(%d)"
    current_app.logger.info(msg, args.page, front_page_item_count)

    paginator = models.Post.get_latest_by_page(
        page=args.page, per_page=front_page_item_count)

    return render_template("index.html", paginator=paginator)


@login_required
def new_url():
    form = forms.Url()

    if form.validate_on_submit():
        title = form.title.data
        url = form.url.data.lower()
        tags = form.tags.data.lower().split(" ")

        msg = u"adding post: title({}) - url({}) - tags({})"
        current_app.logger.info(msg.format(title, url, ','.join(tags)))

        # TODO: set the post categories
        posting = models.Post.create(title, url, tags, [])

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            msg = u"failed to save post: title({}) url({})"
            current_app.logger.exception(msg.format(title, url))

            return redirect(url_for("index"))

        msg = u"Added post: id(%d) title(%s) url(%s)"
        current_app.logger.info(msg, posting.id, title, url)

        return redirect(url_for("index"))

    return render_template("new_url.html", form=form)
