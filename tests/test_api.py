import os
from unittest import TestCase, main
import json

from pagetags.main import create_app
from pagetags import db
from pagetags.models import User, Posting


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
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def add_posting(self, title, url, tags):
        Posting.create(title, url, tags)

        db.session.commit()

    def authenticate(self):
        request_data = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }

        response = self.client.post(
            "/auth",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
            follow_redirects=True
        )

        response = json.loads(response.data)

        return response["access_token"]


class TagsTest(ApiTestCase):
    def test_get_tags(self):
        with self.app.app_context():
            self.add_posting("page 1",
                             "http://www.example.com/page_1",
                             ["tag1", "tag2"])

            self.add_posting("page 2",
                             "http://www.example.com/page_2",
                             ["tag1", "tag3"])

        token = self.authenticate()

        response = self.client.get(
            "/api/v1/tags",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertItemsEqual(response, ["tag1", "tag2", "tag3"])

    def test_get_tag_urls(self):
        with self.app.app_context():
            self.add_posting("page 1",
                             "http://www.example.com/page_1",
                             ["tag1", "tag2"])

            self.add_posting("page 2",
                             "http://www.example.com/page_2",
                             ["tag1", "tag3"])

        token = self.authenticate()

        response = self.client.get(
            "/api/v1/tag/tag1",
            headers={"Authorization": "JWT %s" % token}
        )

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

        response = self.client.get(
            "/api/v1/tag/tag3",
            headers={"Authorization": "JWT %s" % token}
        )

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


class FailtToAccessApPIEndpointWithouTokenTests(ApiTestCase):
    def test_fail_to_access_tags_endpoint_without_token(self):
        response = self.client.get("/api/v1/tag/tag1")

        response = json.loads(response.data)

        self.assertDictEqual(
            response,
            {
                "description": "Request does not contain an access token",
                "error": "Authorization Required",
                "status_code": 401
            }
        )


class ApiAuthenticationTests(ApiTestCase):
    def test_authenticate(self):
        request_data = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }

        response = self.client.post(
            "/auth",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
            follow_redirects=True
        )

        response = json.loads(response.data)

        self.assertIn("access_token", response)
        self.assertIsNotNone(response["access_token"])
        self.assertIsInstance(response["access_token"], unicode)


if __name__ == "__main__":
    main()
