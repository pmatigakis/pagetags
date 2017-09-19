from flask import render_template

from pagetags import reqparsers
from pagetags.models import db, Category


def categories():
    args = reqparsers.categories_posts.parse_args()

    paginator = Category.get_by_page(
        page_num=args.page,
        per_page=args.per_page
    )

    return render_template("categories.html", paginator=paginator)


def category(name):
    args = reqparsers.category_posts.parse_args()

    category_object = Category.get_by_name(db.session, name)

    if category_object is None:
        return render_template("404.html"), 404

    paginator = category_object.get_posts_by_page(
        page=args.page,
        per_page=args.per_page
    )

    return render_template(
        "category.html",
        category=category_object,
        paginator=paginator
    )
