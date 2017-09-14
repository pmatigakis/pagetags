from flask import render_template

from pagetags import reqparsers
from pagetags.models import Category


def categories():
    args = reqparsers.categories_posts.parse_args()

    paginator = Category.get_by_page(
        page_num=args.page,
        per_page=args.per_page
    )

    return render_template("categories.html", paginator=paginator)
