from flask import (render_template, redirect, url_for, request, abort,
                   current_app)
from flask_login import login_required, login_user, logout_user

from pagetags import forms, models, db


@login_required
def index():
    latest_urls = models.Url.get_latest()

    return render_template("index.html", latest_urls=latest_urls)


@login_required
def new_url():
    form = forms.Url()

    if form.validate_on_submit():
        title = form.title.data
        url = form.url.data.lower()
        tags = form.tags.data.lower().split(" ")

        msg = "adding url {} - {} - {}"
        current_app.logger.info(msg.format(title, url, ','.join(tags)))

        url_object = models.Url.get_by_url(url)

        if url_object is None:
            models.Url.create(title, url, tags)
        else:
            url_object.tags = []

            db.session.commit()

            tag_objects = []

            for tag in tags:
                tag = models.Tag.get_or_create(tag)

                db.session.commit()

                tag_objects.append(tag)

            url_object.tags = tag_objects

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("new_url.html", form=form)


@login_required
def tag(name):
    page = request.args.get("page", 1)
    page = int(page)

    msg = "requested page for tag '{}': {}"
    current_app.logger.info(msg.format(name, page))

    tag_object = models.Tag.get_by_name(name)

    if tag_object is None:
        current_app.logger.info("tag '{}' doesn't exist".format(name))
        abort(404)

    paginator = tag_object.get_urls_by_page(page)

    return render_template("tag.html", tag=tag_object, paginator=paginator)


def login():
    form = forms.Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        current_app.logger.info("authenticating user {}".format(username))

        user = models.User.authenticate(username, password)

        if user:
            current_app.logger.info("user {} authenticated".format(username))
            login_user(user)

            return redirect(url_for("index"))
        else:
            msg = "user {} failed to authenticate"
            current_app.logger.warning(msg.format(username))
            abort(401)

    return render_template("login.html", form=form)


@login_required
def logout():
    logout_user()

    return redirect(url_for("login"))
