from flask import render_template, redirect, url_for, request

from pagetags import forms, models, db


def index():
    latest_urls = models.Url.get_latest()

    return render_template("index.html", latest_urls=latest_urls)


def new_url():
    form = forms.Url()

    if form.validate_on_submit():
        url = form.url.data.lower()
        tags = form.tags.data.lower().split(" ")

        tag_objects = []

        for tag in tags:
            tag = models.Tag.get_or_create(tag)

            db.session.commit()

            tag_objects.append(tag)

        url_object = models.Url.get_by_url(url)

        if url_object is None:
            models.Url.create(url, tag_objects)
        else:
            url_object.tags = tag_objects

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("new_url.html", form=form)


def tag(name):
    page = request.args.get("page", 1)
    page = int(page)

    tag_object = models.Tag.get_by_name(name)

    paginator = tag_object.get_urls_by_page(page)

    return render_template("tag.html", tag=tag_object, paginator=paginator)
