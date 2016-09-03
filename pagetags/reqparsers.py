from flask_restful.reqparse import RequestParser


posting = RequestParser()
posting.add_argument("title", required=True, location="json")
posting.add_argument("url", required=True, location="json")
posting.add_argument("tags", required=True, action='append', location="json")


url_query = RequestParser()
url_query.add_argument("url", required=True, location="args")


postings = RequestParser()
postings.add_argument("page", default=1, type=int, location="args")


tag_postings = RequestParser()
tag_postings.add_argument("page", default=1, type=int, location="args")
