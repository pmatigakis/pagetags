from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError

from pagetags import forms, models, db, reqparsers


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

        posting = models.Post.create(title, url, tags)

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


@login_required
def tag(name):
    args = reqparsers.tag_posts.parse_args()

    postings_item_count = current_app.config["TAG_POSTS_PER_PAGE"]

    msg = u"listing posts for tag: tag({}) page({})"
    current_app.logger.info(msg.format(name, args.page))

    tag_object = models.Tag.get_by_name(name)

    if tag_object is None:
        current_app.logger.warning(u"tag doesn't exist: tag({})".format(name))
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
            flash("invalid username or password")

    return render_template("login.html", form=form)


@login_required
def logout():
    msg = u"logging out user {}"
    current_app.logger.info(msg.format(current_user.username))

    logout_user()

    return redirect(url_for("login"))
