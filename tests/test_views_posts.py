from unittest import main

from pagetags import db
from pagetags.models import Post, Url

from common import PagetagsTestWithMockData, PagetagsTestsWithUser


class NewUrlViewTests(PagetagsTestsWithUser):
    def test_new_url(self):
        self.login()

        request_data = {
            "title": "test url",
            "url": "http://www.example.com",
            "tags": "tag1, tag2",
            "categories": "category_1"
        }

        response = self.client.get("/new_url", follow_redirects=True)

        self.assertIn("<title>PageTags - New URL</title>", response.data)

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("test url</a>", response.data)
        self.assertIn("http://www.example.com</a>", response.data)
        self.assertIn("tag1", response.data)
        self.assertIn("tag2", response.data)

        self.logout()

    def test_fail_to_add_post_with_empty_title(self):
        self.login()

        request_data = {
            "title": "",
            "url": "http://www.example.com",
            "tags": "tag1, tag2"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags - New URL</title>", response.data)
        self.assertIn("This field is required", response.data)

        with self.app.app_context():
            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

        self.logout()

    def test_fail_to_add_post_with_empty_url(self):
        self.login()

        request_data = {
            "title": "post title",
            "url": "",
            "tags": "tag1, tag2"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags - New URL</title>", response.data)
        self.assertIn("This field is required", response.data)

        with self.app.app_context():
            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

        self.logout()

    def test_fail_to_add_post_with_large_title(self):
        self.login()

        large_title = "a" * (Post.TITLE_LENGTH + 1)

        request_data = {
            "title": large_title,
            "url": "http://www.example.com",
            "tags": "tag1, tag2"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags - New URL</title>", response.data)

        error_message = "Field cannot be longer than %d characters"
        self.assertIn(error_message % Post.TITLE_LENGTH, response.data)

        with self.app.app_context():
            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

        self.logout()

    def test_fail_to_add_post_with_large_url(self):
        self.login()

        large_url = "http://%s.com" % ("a" * Url.URL_LENGTH)

        request_data = {
            "title": "post title",
            "url": large_url,
            "tags": "tag1, tag2"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags - New URL</title>", response.data)

        error_message = "Field cannot be longer than %d characters"
        self.assertIn(error_message % Url.URL_LENGTH, response.data)

        with self.app.app_context():
            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

        self.logout()


class UrlUpdateTests(PagetagsTestWithMockData):
    def test_tags_are_updated_when_adding_the_url_again(self):
        self.login()

        request_data = {
            "title": "post5",
            "url": "http://www.example.com/page_3",
            "tags": "tag1, tag6",
            "categories": "category_1"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("post5</a>", response.data)
        self.assertIn("http://www.example.com/page_3</a>", response.data)
        self.assertIn("tag1", response.data)
        self.assertIn("tag6", response.data)
        self.assertNotIn("tag7", response.data)
        self.assertIn("category_1", response.data)

        self.logout()


class FrontPageViewtests(PagetagsTestWithMockData):
    def test_front_page(self):
        self.login()

        response = self.client.get("/")

        self.assertIn("<a href=\"/new_url\">New URL</a>", response.data)
        self.assertIn("<a href=\"/logout\">Logout</a>", response.data)

        self.assertIn(
            "<a href=\"http://www.example.com/page_2\">post4</a>",
            response.data
        )

        self.assertIn(
            "<a href=\"http://www.example.com/page_1\">post3</a>",
            response.data
        )

        self.assertIn(
            "<a href=\"http://www.example.com/page_1\">post2</a>",
            response.data
        )

        self.assertNotIn(
            "<a href=\"http://www.example.com/page_1\">post1</a>",
            response.data
        )

        self.assertIn("<a href=\"/tag/tag1\">tag1</a>", response.data)
        self.assertIn("<a href=\"/tag/tag3\">tag3</a>", response.data)
        self.assertIn("<a href=\"/tag/tag4\">tag4</a>", response.data)
        self.assertIn("<a href=\"/tag/tag5\">tag5</a>", response.data)
        self.assertIn("<a href=\"/tag/tag2\">tag2</a>", response.data)

        self.assertIn("<a href=\"/?page=2\">Next</a>", response.data)
        self.assertNotIn("<a href=\"/?page=0\">Previous</a>", response.data)

        self.logout()

    def test_front_page_page_2(self):
        self.login()

        response = self.client.get("/?page=2")

        self.assertIn("<a href=\"/new_url\">New URL</a>", response.data)
        self.assertIn("<a href=\"/logout\">Logout</a>", response.data)

        self.assertNotIn(
            "post4",
            response.data
        )

        self.assertNotIn(
            "post3",
            response.data
        )

        self.assertNotIn(
            "post3",
            response.data
        )

        self.assertIn(
            "post1",
            response.data
        )

        self.assertIn("<a href=\"/tag/tag1\">tag1</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag3\">tag3</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag4\">tag4</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag5\">tag5</a>", response.data)
        self.assertIn("<a href=\"/tag/tag2\">tag2</a>", response.data)

        self.assertNotIn("<a href=\"/?page=2\">Next</a>", response.data)
        self.assertIn("<a href=\"/?page=1\">Previous</a>", response.data)

        self.logout()


if __name__ == "__main__":
    main()
