from flask_restful.reqparse import RequestParser


post = RequestParser()
post.add_argument("title", required=True, location="json")
post.add_argument("url", required=True, location="json")
post.add_argument("tags", required=True, action='append', location="json")


url_query = RequestParser()
url_query.add_argument("url", required=True, location="args")


posts = RequestParser()
posts.add_argument("page", default=1, type=int, location="args")


tag_posts = RequestParser()
tag_posts.add_argument("page", default=1, type=int, location="args")
