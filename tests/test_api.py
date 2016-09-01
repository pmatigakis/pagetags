import os
from unittest import TestCase, main
import json
import urllib

from pagetags.main import create_app
from pagetags import db
from pagetags.models import Posting

from mock_data import load_users, load_mock_postings


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
        self.PASSWORD = "user1-password"

        with self.app.app_context():
            db.create_all()
            load_users(db)

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
    def setUp(self):
        super(TagsTest, self).setUp()

        with self.app.app_context():
            load_mock_postings(db)

    def test_get_tags(self):
        token = self.authenticate()

        response = self.client.get(
            "/api/v1/tags",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertItemsEqual(response, ["tag1", "tag2", "tag3"])

    def test_get_tag_urls(self):
        token = self.authenticate()

        response = self.client.get(
            "/api/v1/tag/tag1",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertEqual(len(response), 3)

        self.assertDictEqual(
            response[0],
            {
                "id": 1,
                "title": "page 1",
                "url": "http://www.example.com/page_1",
                "tags": ["tag1", "tag2"]
            }
        )

        self.assertDictEqual(
            response[1],
            {
                "id": 2,
                "title": "page 2",
                "url": "http://www.example.com/page_2",
                "tags": ["tag1", "tag3"]
            }
        )

        self.assertDictEqual(
            response[2],
            {
                "id": 3,
                "title": "page 3",
                "url": "http://www.example.com/page_1",
                "tags": ["tag1", "tag3"]
            }
        )

        response = self.client.get(
            "/api/v1/tag/tag2",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertEqual(len(response), 1)

        self.assertDictEqual(
            response[0],
            {
                "id": 1,
                "title": "page 1",
                "url": "http://www.example.com/page_1",
                "tags": ["tag1", "tag2"]
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


class PostingApiTests(ApiTestCase):
    def test_add_posting(self):
        token = self.authenticate()

        posting = {
            "title": "posting title",
            "url": "http://www.example.com",
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/postings",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertIsNotNone(response.get("id"))


class UrlAPIEndpointTests(ApiTestCase):
    def setUp(self):
        super(UrlAPIEndpointTests, self).setUp()

        with self.app.app_context():
            load_mock_postings(db)

    def test_retrieve_postings_by_url(self):
        token = self.authenticate()

        url = "http://www.example.com/page_1"

        response = self.client.get(
            "/api/v1/url?%s" % urllib.urlencode({"url": url}),
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertEqual(len(response), 2)

        self.assertEqual(response[0]["id"], 3)
        self.assertEqual(response[0]["title"], "page 3")
        self.assertEqual(response[0]["url"], url)
        self.assertItemsEqual(response[0]["tags"], ["tag1", "tag3"])
        self.assertIsNotNone(response[0]["added_at"])

        self.assertEqual(response[1]["id"], 1)
        self.assertEqual(response[1]["title"], "page 1")
        self.assertEqual(response[1]["url"], url)
        self.assertItemsEqual(response[1]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(response[1]["added_at"])


if __name__ == "__main__":
    main()
