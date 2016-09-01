import os
from unittest import TestCase, main

from pagetags.main import create_app
from pagetags import db

from mock_data import load_users, load_mock_postings


class WebTestCase(TestCase):
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

    def login(self):
        request_data = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }

        response = self.client.post("/login",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)

    def logout(self):
        response = self.client.get("/logout", follow_redirects=True)

        self.assertIn("<title>PageTags - Login</title>", response.data)

    def add_url(self, title, url, tags):
        request_data = {
            "title": title,
            "url": url,
            "tags": " ".join(tags)
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("%s</a>" % title, response.data)
        self.assertIn("%s</a>" % url, response.data)

        for tag in tags:
            self.assertIn(tag, response.data)


class LoginTests(WebTestCase):
    def test_login(self):
        client = self.app.test_client()

        request_data = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }

        response = client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = client.post("/login",
                               data=request_data,
                               follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("New URL", response.data)
        self.assertIn("Logout", response.data)

    def test_login_then_logout(self):
        client = self.app.test_client()

        request_data = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }

        response = client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = client.post("/login",
                               data=request_data,
                               follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("New URL", response.data)
        self.assertIn("Logout", response.data)

        response = client.get("/logout", follow_redirects=True)

        self.assertIn("<title>PageTags - Login</title>", response.data)


class NewUrlViewTests(WebTestCase):
    def test_new_url(self):
        self.login()

        request_data = {
            "title": "test url",
            "url": "http://www.example.com",
            "tags": "tag1, tag2"
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


class UrlUpdateTests(WebTestCase):
    def setUp(self):
        super(UrlUpdateTests, self).setUp()

        with self.app.app_context():
            load_mock_postings(db)

    def test_tags_are_updated_when_adding_the_url_again(self):
        self.login()

        request_data = {
            "title": "test url",
            "url": "http://www.example.com/page_1",
            "tags": "tag1, tag4"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("test url</a>", response.data)
        self.assertIn("http://www.example.com/page_1</a>", response.data)
        self.assertIn("tag1", response.data)
        self.assertIn("tag2", response.data)
        self.assertIn("tag3", response.data)
        self.assertIn("tag4", response.data)

        self.logout()


class TagViewTests(WebTestCase):
    def setUp(self):
        super(TagViewTests, self).setUp()

        with self.app.app_context():
            load_mock_postings(db)

    def test_view_tag(self):
        self.login()

        response = self.client.get("/tag/tag1")

        self.assertIn("<title>PageTags - Tag - tag1</title>", response.data)

        self.assertIn("page 1</a>", response.data)
        self.assertIn("http://www.example.com/page_1\">", response.data)

        self.assertIn("page 2</a>", response.data)
        self.assertIn("http://www.example.com/page_2\">", response.data)

        self.assertIn("page 3</a>", response.data)

        response = self.client.get("/tag/tag2")

        self.assertIn("<title>PageTags - Tag - tag2</title>", response.data)

        self.assertNotIn("page 2</a>", response.data)
        self.assertNotIn("http://www.example.com/page_2\">", response.data)

        self.assertIn("page 1</a>", response.data)
        self.assertIn("http://www.example.com/page_1\">", response.data)

        self.logout()

    def test_do_not_raise_an_error_if_tag_does_not_exist(self):
        self.login()

        response = self.client.get("/tag/tag4")

        self.assertIn("<title>404 Not Found</title>", response.data)

        self.logout()


if __name__ == "__main__":
    main()
