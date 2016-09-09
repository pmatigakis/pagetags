import json
from unittest import TestCase, main

from flask import Flask

from pagetags import reqparsers


class PostArgumentParserTests(TestCase):
    def test_parser_post_arguments(self):
        app = Flask(__name__)

        with app.test_request_context(
                "/api/v1/posts",
                method="POST",
                content_type="application/json",
                data=json.dumps(
                    {"title": "hello world",
                     "url": "http://www.example.com",
                     "tags": ["tag1", "tag2"]})):
            args = reqparsers.post.parse_args()

            self.assertEqual(args.title, "hello world")
            self.assertEqual(args.url, "http://www.example.com")
            self.assertItemsEqual(args.tags, ["tag1", "tag2"])


if __name__ == "__main__":
    main()
