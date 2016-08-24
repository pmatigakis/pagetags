import os
from unittest import TestCase, main

from pagetags.main import create_app
from pagetags import db
from pagetags.models import User


class LoginTests(TestCase):
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

    def tearDown(self):
        try:
            os.remove(self.db_path)
        except:
            pass

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

    def test_tags_are_updated_when_addign_the_url_again(self):
        self.login()

        request_data = {
            "title": "test url",
            "url": "http://www.example.com",
            "tags": "tag1, tag2"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("test url</a>", response.data)
        self.assertIn("http://www.example.com</a>", response.data)
        self.assertIn("tag1", response.data)
        self.assertIn("tag2", response.data)

        request_data = {
            "title": "test url",
            "url": "http://www.example.com",
            "tags": "tag1, tag3"
        }

        response = self.client.post("/new_url",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)
        self.assertIn("test url</a>", response.data)
        self.assertIn("http://www.example.com</a>", response.data)
        self.assertIn("tag1", response.data)
        self.assertNotIn("tag2", response.data)
        self.assertIn("tag3", response.data)

        self.logout()


class TagViewTests(WebTestCase):
    def test_view_tag(self):
        self.login()

        self.add_url("test page 1", "http://www.example.com/page_1",
                     ["tag1", "tag2"])

        self.add_url("test page 2", "http://www.example.com/page_2",
                     ["tag1", "tag3"])

        response = self.client.get("/tag/tag1")

        self.assertIn("<title>PageTags - Tag - tag1</title>", response.data)

        self.assertIn("test page 1</a>", response.data)
        self.assertIn("http://www.example.com/page_1\">", response.data)

        self.assertIn("test page 2</a>", response.data)
        self.assertIn("http://www.example.com/page_2\">", response.data)

        response = self.client.get("/tag/tag3")

        self.assertIn("<title>PageTags - Tag - tag3</title>", response.data)

        self.assertNotIn("test page 1</a>", response.data)
        self.assertNotIn("http://www.example.com/page_1\">", response.data)

        self.assertIn("test page 2</a>", response.data)
        self.assertIn("http://www.example.com/page_2\">", response.data)

        self.logout()

    def test_do_not_raise_an_error_if_tag_does_not_exist(self):
        self.login()

        response = self.client.get("/tag/tag1")

        self.assertIn("<title>404 Not Found</title>", response.data)

        self.logout()


if __name__ == "__main__":
    main()
