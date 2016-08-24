import os
from unittest import TestCase, main
import json

from pagetags.main import create_app
from pagetags import db
from pagetags.models import User, Url


class ApiTestCase(TestCase):
    def setUp(self):
        settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "settings.py")

        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_pagetags.db")

        try:
            os.remove(self.db_path)
        except:
            pass

        self.app = create_app(settings_file, "testing")

        self.USERNAME = "user1"
        self.PASSWORD = "password"

        with self.app.app_context():
            db.create_all()

            User.create(self.USERNAME, self.PASSWORD)
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        try:
            os.remove(self.db_path)
        except:
            pass

    def add_url(self, title, url, tags):
        Url.create(title, url, tags)

        db.session.commit()


class TagsTest(ApiTestCase):
    def test_get_tags(self):
        with self.app.app_context():
            self.add_url("page 1",
                         "http://www.example.com/page_1",
                         ["tag1", "tag2"])

            self.add_url("page 2",
                         "http://www.example.com/page_2",
                         ["tag1", "tag3"])

        response = self.client.get("/api/v1/tags")

        response = json.loads(response.data)

        self.assertItemsEqual(response, ["tag1", "tag2", "tag3"])

    def test_get_tag_urlss(self):
        with self.app.app_context():
            self.add_url("page 1",
                         "http://www.example.com/page_1",
                         ["tag1", "tag2"])

            self.add_url("page 2",
                         "http://www.example.com/page_2",
                         ["tag1", "tag3"])

        response = self.client.get("/api/v1/tag/tag1")

        response = json.loads(response.data)

        self.assertEqual(len(response), 2)

        self.assertDictEqual(
            response[0],
            {
                "id": 1,
                "title": "page 1",
                "url": "http://www.example.com/page_1"
            }
        )

        self.assertDictEqual(
            response[1],
            {
                "id": 2,
                "title": "page 2",
                "url": "http://www.example.com/page_2"
            }
        )

        response = self.client.get("/api/v1/tag/tag3")

        response = json.loads(response.data)

        self.assertEqual(len(response), 1)

        self.assertDictEqual(
            response[0],
            {
                "id": 2,
                "title": "page 2",
                "url": "http://www.example.com/page_2"
            }
        )


if __name__ == "__main__":
    main()
