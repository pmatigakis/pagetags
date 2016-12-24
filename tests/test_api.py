from unittest import main
import json
import urllib

import jwt

from pagetags.models import Post, Url

from common import PagetagsTestWithMockData


class TagsTest(PagetagsTestWithMockData):
    def test_get_tags(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/tags",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertItemsEqual(response,
                              ["tag1", "tag2", "tag3", "tag4", "tag5"])

    def test_get_tag_urls(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/tag/tag2",
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertEqual(response["page"], 1)
        self.assertEqual(response["per_page"], 10)
        self.assertEqual(len(response["posts"]), 2)
        self.assertFalse(response["has_more"])

        self.assertEqual(response["posts"][0]["id"], 4)
        self.assertEqual(response["posts"][0]["title"], "post4")
        self.assertEqual(
            response["posts"][0]["url"], "http://www.example.com/page_2")
        self.assertItemsEqual(
            response["posts"][0]["tags"], ["tag1", "tag2", "tag5"])
        self.assertIsNotNone(response["posts"][0]["added_at"])

        self.assertEqual(response["posts"][1]["id"], 1)
        self.assertEqual(response["posts"][1]["title"], "post1")
        self.assertEqual(
            response["posts"][1]["url"], "http://www.example.com/page_1")
        self.assertItemsEqual(response["posts"][1]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(response["posts"][1]["added_at"])

    def test_get_tag_posts_by_page(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        endpoint_url = "/api/v1/tag/tag1?%s" % urllib.urlencode(
            {"page": 1, "per_page": 2})

        response = self.client.get(
            endpoint_url,
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertEqual(response["page"], 1)
        self.assertEqual(response["per_page"], 2)
        self.assertEqual(len(response["posts"]), 2)
        self.assertTrue(response["has_more"])

        self.assertEqual(response["posts"][0]["id"], 4)
        self.assertEqual(response["posts"][0]["title"], "post4")
        self.assertEqual(
            response["posts"][0]["url"], "http://www.example.com/page_2")
        self.assertItemsEqual(
            response["posts"][0]["tags"], ["tag1", "tag2", "tag5"])
        self.assertIsNotNone(response["posts"][0]["added_at"])

        self.assertEqual(response["posts"][1]["id"], 3)
        self.assertEqual(response["posts"][1]["title"], "post3")
        self.assertEqual(
            response["posts"][1]["url"], "http://www.example.com/page_1")
        self.assertItemsEqual(response["posts"][1]["tags"], ["tag1", "tag4"])
        self.assertIsNotNone(response["posts"][1]["added_at"])

    def test_get_second_page_of_tag_posts(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        endpoint_url = "/api/v1/tag/tag1?%s" % urllib.urlencode(
            {"page": 2, "per_page": 2})

        response = self.client.get(
            endpoint_url,
            headers={"Authorization": "JWT %s" % token}
        )

        response = json.loads(response.data)

        self.assertEqual(response["page"], 2)
        self.assertEqual(response["per_page"], 2)
        self.assertEqual(len(response["posts"]), 2)
        self.assertFalse(response["has_more"])

        self.assertEqual(response["posts"][0]["id"], 2)
        self.assertEqual(response["posts"][0]["title"], "post2")
        self.assertEqual(
            response["posts"][0]["url"], "http://www.example.com/page_1")
        self.assertItemsEqual(response["posts"][0]["tags"], ["tag1", "tag3"])
        self.assertIsNotNone(response["posts"][0]["added_at"])

        self.assertEqual(response["posts"][1]["id"], 1)
        self.assertEqual(response["posts"][1]["title"], "post1")
        self.assertEqual(
            response["posts"][1]["url"], "http://www.example.com/page_1")
        self.assertItemsEqual(response["posts"][1]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(response["posts"][1]["added_at"])

    def test_fail_to_get_page_of_tag_posts_that_does_not_exist(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        endpoint_url = "/api/v1/tag/tag111?%s" % urllib.urlencode(
            {"page": 3, "per_page": 2})

        client = self.app.test_client()

        response = client.get(
            endpoint_url,
            headers={"Authorization": "JWT %s" % token}
        )

        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                'error': "tag doesn't exist",
                'error_code': 1000,
                'tag': 'tag111'
             }
        )


class FailtToAccessApPIEndpointWithouTokenTests(PagetagsTestWithMockData):
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


class ApiAuthenticationTests(PagetagsTestWithMockData):
    def test_authenticate(self):
        request_data = {
            "username": self.test_user_username,
            "password": self.test_user_password
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


class PostApiTests(PagetagsTestWithMockData):
    def test_add_posting(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        posting = {
            "title": "posting title",
            "url": "http://www.example.com",
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertIsNotNone(response.get("id"))

    def test_fail_to_add_post_with_empty_title(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        posting = {
            "title": "",
            "url": "http://www.example.com",
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.data)

        self.assertDictEqual(
            response_data,
            {u'message': {u'title': u'A title is required'}}
        )

    def test_fail_to_add_post_with_empty_url(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        posting = {
            "title": "post title",
            "url": "",
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.data)

        self.assertDictEqual(
            response_data,
            {u'message': {u'url': u'A url is required'}}
        )

    def test_fail_to_add_post_with_large_title(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        large_title = "a" * (Post.TITLE_LENGTH + 1)

        posting = {
            "title": large_title,
            "url": "http://www.example.com",
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.data)

        self.assertDictEqual(
            response_data,
            {u'message': {
                u'title': u'The title length is over the maximum allowed'}}
        )

    def test_fail_to_add_post_with_large_url(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        large_url = "http://%s.com" % ("a" * Url.URL_LENGTH)

        posting = {
            "title": "post title",
            "url": large_url,
            "tags": ["tag1", "tag2"]
        }

        response = self.client.post(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
            data=json.dumps(posting)
        )

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.data)

        self.assertDictEqual(
            response_data,
            {u'message': {
                u'url': u'The url length is over the maximum allowed'}}
        )


class UrlAPIEndpointTests(PagetagsTestWithMockData):
    def test_retrieve_postings_by_url(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        url = "http://www.example.com/page_1"

        response = self.client.get(
            "/api/v1/url?%s" % urllib.urlencode({"url": url}),
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertFalse(response["has_more"])
        self.assertEqual(response["page"], 1)
        self.assertEqual(response["per_page"], 10)
        self.assertEqual(len(response["posts"]), 3)

        self.assertEqual(response["posts"][0]["id"], 3)
        self.assertEqual(response["posts"][0]["title"], "post3")
        self.assertEqual(response["posts"][0]["url"], url)
        self.assertItemsEqual(response["posts"][0]["tags"], ["tag1", "tag4"])
        self.assertIsNotNone(response["posts"][0]["added_at"])

        self.assertEqual(response["posts"][1]["id"], 2)
        self.assertEqual(response["posts"][1]["title"], "post2")
        self.assertEqual(response["posts"][1]["url"], url)
        self.assertItemsEqual(response["posts"][1]["tags"], ["tag1", "tag3"])
        self.assertIsNotNone(response["posts"][1]["added_at"])

        self.assertEqual(response["posts"][2]["id"], 1)
        self.assertEqual(response["posts"][2]["title"], "post1")
        self.assertEqual(response["posts"][2]["url"], url)
        self.assertItemsEqual(response["posts"][2]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(response["posts"][2]["added_at"])

    def test_retrieve_url_post_by_page(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        url = "http://www.example.com/page_1"

        response = self.client.get(
            "/api/v1/url?%s" % urllib.urlencode(
                {"url": url, "page": 1, "per_page": 1}),
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertTrue(response["has_more"])
        self.assertEqual(response["page"], 1)
        self.assertEqual(response["per_page"], 1)
        self.assertEqual(len(response["posts"]), 1)

        self.assertEqual(response["posts"][0]["id"], 3)
        self.assertEqual(response["posts"][0]["title"], "post3")
        self.assertEqual(response["posts"][0]["url"], url)
        self.assertItemsEqual(response["posts"][0]["tags"], ["tag1", "tag4"])
        self.assertIsNotNone(response["posts"][0]["added_at"])

    def test_retrieve_second_page_of_url_posts(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        url = "http://www.example.com/page_1"

        response = self.client.get(
            "/api/v1/url?%s" % urllib.urlencode(
                {"url": url, "page": 2, "per_page": 2}),
            headers={"Authorization": "JWT %s" % token,
                     "Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)

        self.assertFalse(response["has_more"])
        self.assertEqual(response["page"], 2)
        self.assertEqual(response["per_page"], 2)
        self.assertEqual(len(response["posts"]), 1)

        self.assertEqual(response["posts"][0]["id"], 1)
        self.assertEqual(response["posts"][0]["title"], "post1")
        self.assertEqual(response["posts"][0]["url"], url)
        self.assertItemsEqual(response["posts"][0]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(response["posts"][0]["added_at"])


class APIPostRetrievalTests(PagetagsTestWithMockData):
    def test_get_latest_posts(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/posts",
            headers={"Authorization": "JWT %s" % token}
        )

        data = json.loads(response.data)

        self.assertEqual(data["page"], 1)
        self.assertEqual(data["per_page"], 10)
        self.assertFalse(data["has_more"])

        self.assertEqual(len(data["posts"]), 4)

        self.assertEqual(data["posts"][0]["id"], 4)
        self.assertEqual(data["posts"][0]["title"], "post4")

        self.assertEqual(
            data["posts"][0]["url"], "http://www.example.com/page_2")

        self.assertItemsEqual(
            data["posts"][0]["tags"], ["tag1", "tag2", "tag5"])
        self.assertIsNotNone(data["posts"][0]["added_at"])

        self.assertEqual(data["posts"][1]["id"], 3)
        self.assertEqual(data["posts"][1]["title"], "post3")

        self.assertEqual(
            data["posts"][1]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][1]["tags"], ["tag1", "tag4"])
        self.assertIsNotNone(data["posts"][1]["added_at"])

        self.assertEqual(data["posts"][2]["id"], 2)
        self.assertEqual(data["posts"][2]["title"], "post2")

        self.assertEqual(
            data["posts"][2]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][2]["tags"], ["tag1", "tag3"])
        self.assertIsNotNone(data["posts"][2]["added_at"])

        self.assertEqual(data["posts"][3]["id"], 1)
        self.assertEqual(data["posts"][3]["title"], "post1")

        self.assertEqual(
            data["posts"][3]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][3]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(data["posts"][3]["added_at"])

    def test_get_first_page_of_posts(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/posts?%s" % urllib.urlencode({"page": 1, "per_page": 2}),
            headers={"Authorization": "JWT %s" % token}
        )

        data = json.loads(response.data)

        self.assertEqual(data["page"], 1)
        self.assertEqual(data["per_page"], 2)
        self.assertTrue(data["has_more"])

        self.assertEqual(len(data["posts"]), 2)

        self.assertEqual(data["posts"][0]["id"], 4)
        self.assertEqual(data["posts"][0]["title"], "post4")

        self.assertEqual(
            data["posts"][0]["url"], "http://www.example.com/page_2")

        self.assertItemsEqual(
            data["posts"][0]["tags"], ["tag1", "tag2", "tag5"])
        self.assertIsNotNone(data["posts"][0]["added_at"])

        self.assertEqual(data["posts"][1]["id"], 3)
        self.assertEqual(data["posts"][1]["title"], "post3")

        self.assertEqual(
            data["posts"][1]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][1]["tags"], ["tag1", "tag4"])
        self.assertIsNotNone(data["posts"][1]["added_at"])

    def test_get_second_page_of_posts(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/posts?%s" % urllib.urlencode({"page": 2, "per_page": 2}),
            headers={"Authorization": "JWT %s" % token}
        )

        data = json.loads(response.data)

        self.assertEqual(data["page"], 2)
        self.assertEqual(data["per_page"], 2)
        self.assertFalse(data["has_more"])

        self.assertEqual(len(data["posts"]), 2)

        self.assertEqual(data["posts"][0]["id"], 2)
        self.assertEqual(data["posts"][0]["title"], "post2")

        self.assertEqual(
            data["posts"][0]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][0]["tags"], ["tag1", "tag3"])
        self.assertIsNotNone(data["posts"][0]["added_at"])

        self.assertEqual(data["posts"][1]["id"], 1)
        self.assertEqual(data["posts"][1]["title"], "post1")

        self.assertEqual(
            data["posts"][1]["url"], "http://www.example.com/page_1")

        self.assertItemsEqual(data["posts"][1]["tags"], ["tag1", "tag2"])
        self.assertIsNotNone(data["posts"][1]["added_at"])

    def test_get_error_when_requesting_page_that_does_not_exist(self):
        token = self.authenticate(
            self.test_user_username, self.test_user_password)

        response = self.client.get(
            "/api/v1/posts?%s" % urllib.urlencode({"page": 3, "per_page": 2}),
            headers={"Authorization": "JWT %s" % token}
        )

        self.assertEqual(response.status_code, 404)


class AuthenticationTests(PagetagsTestWithMockData):
    def test_authenticate(self):
        request_data = {
            "username": self.test_user_username,
            "password": self.test_user_password
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

        payload = jwt.decode(response["access_token"], verify=False)

        self.assertIn("identity", payload)
        self.assertIn("jti", payload)
        self.assertIsNotNone(payload["identity"])
        self.assertIsNotNone(payload["jti"])


if __name__ == "__main__":
    main()
