from flask_restful.reqparse import RequestParser

from pagetags import argtypes


post = RequestParser()
post.add_argument("title", required=True, location="json",
                  type=argtypes.post_title)
post.add_argument("url", required=True, location="json",
                  type=argtypes.post_url)
post.add_argument("tags", required=True, type=list, location="json")
post.add_argument("categories", required=True, type=list, location="json")


url_query = RequestParser()
url_query.add_argument("url", required=True, location="args")
url_query.add_argument("page", default=1, type=int, location="args")
url_query.add_argument("per_page", default=10, type=int, location="args")


posts = RequestParser()
posts.add_argument("page", default=1, type=int, location="args")
posts.add_argument("per_page", default=10, type=int, location="args")


tag_posts = RequestParser()
tag_posts.add_argument("page", default=1, type=int, location="args")
tag_posts.add_argument("per_page", default=10, type=int, location="args")


tags_posts = RequestParser()
tags_posts.add_argument("page", default=1, type=int, location="args")
tags_posts.add_argument("per_page", default=10, type=int, location="args")


update_post = RequestParser()
update_post.add_argument(
    "title", required=True, location="json", type=argtypes.post_title)
update_post.add_argument(
    "url", required=True, location="json", type=argtypes.post_url)
update_post.add_argument("tags", required=True, type=list, location="json")


categories_posts = RequestParser()
categories_posts.add_argument("page", default=1, type=int, location="args")
categories_posts.add_argument(
    "per_page", default=10, type=int, location="args")


category_posts = RequestParser()
category_posts.add_argument("page", default=1, type=int, location="args")
category_posts.add_argument("per_page", default=10, type=int, location="args")


categories = RequestParser()
categories.add_argument("page", default=1, type=int, location="args")
categories.add_argument("per_page", default=10, type=int, location="args")
