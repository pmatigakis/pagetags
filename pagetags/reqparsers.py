from flask_restful.reqparse import RequestParser


posting = RequestParser()
posting.add_argument("title", required=True, location="json")
posting.add_argument("url", required=True, location="json")
posting.add_argument("tags", required=True, action='append', location="json")


url_query = RequestParser()
url_query = url_query.add_argument("url", required=True, location="args")
