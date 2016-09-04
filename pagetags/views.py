from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError

from pagetags import forms, models, db, reqparsers


@login_required
def index():
    front_page_item_count = current_app.config["FRONT_PAGE_ITEM_COUNT"]

    args = reqparsers.posts.parse_args()

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

        msg = u"adding url {} - {} - {}"
        current_app.logger.info(msg.format(title, url, ','.join(tags)))

        posting = models.Post.create(title, url, tags)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception(u"failed to save url {}".format(url))

        current_app.logger.debug("Added posting with id %d", posting.id)

        return redirect(url_for("index"))

    return render_template("new_url.html", form=form)


@login_required
def tag(name):
    args = reqparsers.tag_posts.parse_args()

    postings_item_count = current_app.config["TAG_POSTS_PER_PAGE"]

    msg = u"requested page for tag '{}': {}"
    current_app.logger.info(msg.format(name, args.page))

    tag_object = models.Tag.get_by_name(name)

    if tag_object is None:
        current_app.logger.info(u"tag '{}' doesn't exist".format(name))
        abort(404)

    paginator = tag_object.get_posts_by_page(
        args.page, per_page=postings_item_count)

    return render_template("tag.html", tag=tag_object, paginator=paginator)


def login():
    form = forms.Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        current_app.logger.info(u"authenticating user {}".format(username))

        user = models.User.authenticate(username, password)

        if user:
            current_app.logger.info(u"user {} authenticated".format(username))
            login_user(user)

            return redirect(url_for("index"))
        else:
            msg = u"user {} failed to authenticate"
            current_app.logger.warning(msg.format(username))
            abort(401)

    return render_template("login.html", form=form)


@login_required
def logout():
    msg = u"logging out user {}"
    current_app.logger.info(msg.format(current_user.username))

    logout_user()

    return redirect(url_for("login"))
