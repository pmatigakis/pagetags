import os
from unittest import TestCase
from datetime import datetime
import json

from sqlalchemy.exc import SQLAlchemyError

from pagetags.main import create_app
from pagetags import db
from pagetags.models import User, Post, Category, PostCategory


class PagetagsTest(TestCase):
    def setUp(self):
        settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "settings.py")

        self.app = create_app(settings_file, "testing")

        with self.app.app_context():
            try:
                db.drop_all()
                db.create_all()
            except Exception:
                self.fail("failed to initialize test case")

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

    def authenticate(self, username, password):
        request_data = {
            "username": username,
            "password": password
        }

        response = self.client.post(
            "/auth",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
            follow_redirects=True
        )

        response = json.loads(response.data)

        return response["access_token"]

    def login(self):
        request_data = {
            "username": self.test_user_username,
            "password": self.test_user_password
        }

        response = self.client.post("/login",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)

    def logout(self):
        response = self.client.get("/logout", follow_redirects=True)

        self.assertIn("<title>PageTags - Login</title>", response.data)


class PagetagsTestsWithUser(PagetagsTest):
    def setUp(self):
        super(PagetagsTestsWithUser, self).setUp()

        with self.app.app_context():
            user = User.create("user1", "password")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to load mock data")

            self.test_user_id = user.id
            self.test_user_username = user.username
            self.test_user_jti = user.jti
            self.test_user_password = "password"


class PagetagsTestWithMockData(PagetagsTestsWithUser):
    def setUp(self):
        super(PagetagsTestWithMockData, self).setUp()

        with self.app.app_context():
            post1 = Post.create("post1", "http://www.example.com/page_1",
                                ["tag1", "tag2"], [])
            post1.added_at = datetime(2016, 10, 5, 12, 30, 0)
            post1.id = 1

            post2 = Post.create("post2", "http://www.example.com/page_1",
                                ["tag1", "tag3"], [])
            post2.added_at = datetime(2016, 10, 5, 12, 31, 0)
            post2.id = 2

            post3 = Post.create("post3", "http://www.example.com/page_1",
                                ["tag1", "tag4"], [])
            post3.added_at = datetime(2016, 10, 5, 12, 32, 0)
            post3.id = 3

            post4 = Post.create("post4", "http://www.example.com/page_2",
                                ["tag1", "tag2", "tag5"], [])
            post4.added_at = datetime(2016, 10, 5, 12, 33, 0)
            post4.id = 4

            category1 = Category.create("category_1")
            category1.id = 1
            category1.added_at = datetime(2016, 10, 1, 12, 0, 0)

            category2 = Category.create("category_2")
            category2.id = 2
            category2.added_at = datetime(2016, 10, 2, 12, 0, 0)

            post_category = PostCategory(
                post=post4,
                category=category1
            )

            db.session.add(post_category)

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to load mock data")
