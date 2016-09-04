import os
from unittest import TestCase, main
import time

from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash
from pagetags.main import create_app
from pagetags.models import User, Tag, Post, Url
from pagetags import db

from mock_data import load_mock_posts


class UserCreationModelTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(User).count(), 0)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_create_user(self):
        with self.app.app_context():
            user = User.create("user1", "password")

            self.assertIsNone(user.id)
            self.assertEqual(user.username, "user1")
            self.assertTrue(check_password_hash(user.password, "password"))

            db.session.commit()

            self.assertIsNotNone(user.id)

    def test_fail_to_create_user_using_existing_username(self):
        with self.app.app_context():
            User.create("user1", "password")

            db.session.commit()

            User.create("user1", "password")

            self.assertRaises(IntegrityError, db.session.commit)


class UserRetrievalTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(User).count(), 0)

            User.create("user1", "password")

            db.session.commit()

            self.assertEqual(db.session.query(User).count(), 1)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_get_user_by_username(self):
        with self.app.app_context():
            user = User.get_by_username("user1")

            self.assertIsNotNone(user)
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "user1")
            self.assertTrue(check_password_hash(user.password, "password"))

    def test_fail_to_get_user_that_doesnt_exist(self):
        with self.app.app_context():
            user = User.get_by_username("user2")

            self.assertIsNone(user)


class UserDeletionTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(User).count(), 0)

            User.create("user1", "password")

            db.session.commit()

            self.assertEqual(db.session.query(User).count(), 1)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_delete_user(self):
        with self.app.app_context():
            user = User.delete("user1")

            self.assertIsNotNone(user)
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "user1")

            db.session.commit()

            self.assertEqual(db.session.query(User).count(), 0)


class UserPasswordTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(User).count(), 0)

            User.create("user1", "password")

            db.session.commit()

            self.assertEqual(db.session.query(User).count(), 1)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_change_user_password(self):
        with self.app.app_context():
            user = User.get_by_username("user1")

            user.change_password("password1")

            db.session.commit()

            user = User.get_by_username("user1")

            self.assertTrue(check_password_hash(user.password, "password1"))


class UserAuthenticationTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(User).count(), 0)

            User.create("user1", "password")

            db.session.commit()

            self.assertEqual(db.session.query(User).count(), 1)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_authenticate(self):
        with self.app.app_context():
            self.assertTrue(User.authenticate("user1", "password"))

    def test_fail_to_authenticate_with_invalid_password(self):
        with self.app.app_context():
            self.assertFalse(User.authenticate("user1", "password1"))

    def test_fail_to_authenticate_unknown_user(self):
        with self.app.app_context():
            self.assertFalse(User.authenticate("user2", "password"))


class TagCreationTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(Tag).count(), 0)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_create_tag(self):
        with self.app.app_context():
            tag = Tag.create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNone(tag.id)
            self.assertEqual(tag.name, "tag1")

            db.session.commit()

            self.assertIsNotNone(tag.id)

    def test_fail_to_create_duplicate_tag(self):
        with self.app.app_context():
            Tag.create("tag1")

            db.session.commit()

            Tag.create("tag1")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_tag(self):
        with self.app.app_context():
            tag = Tag.get_or_create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNone(tag.id)
            self.assertEqual(tag.name, "tag1")

            db.session.commit()

            self.assertIsNotNone(tag.id)

    def test_get_or_create_existing_tag(self):
        with self.app.app_context():
            Tag.create("tag1")

            db.session.commit()

            tag = Tag.get_or_create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.id)
            self.assertEqual(tag.name, "tag1")


class UrlCreationTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(Url).count(), 0)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_create_url(self):
        with self.app.app_context():
            url = Url.create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

            db.session.commit()

            self.assertIsNotNone(url.id)

    def test_fail_to_create_duplicate_url(self):
        with self.app.app_context():
            Url.create("http://www.example.com")

            db.session.commit()

            Url.create("http://www.example.com")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_url(self):
        with self.app.app_context():
            url = Url.get_or_create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

            db.session.commit()

            self.assertIsNotNone(url.id)

    def test_get_or_create_existing_url(self):
        with self.app.app_context():
            Url.create("http://www.example.com")

            db.session.commit()

            url = Url.get_or_create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNotNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")


class PostCreationTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Tag).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_create_posting(self):
        with self.app.app_context():
            post = Post.create(
                "post title",
                "http://www.example.com",
                ["tag1", "tag2"]
            )

            self.assertIsNotNone(post)
            self.assertIsNone(post.id)
            self.assertEqual(post.title, "post title")
            self.assertEqual(post.url.url, "http://www.example.com")
            self.assertItemsEqual(
                [tag.name for tag in post.tags],
                ["tag1", "tag2"]
            )

            db.session.commit()

            self.assertIsNotNone(post.id)

    def test_post_name_tags(self):
        with self.app.app_context():
            post = Post.create(
                "post title",
                "http://www.example.com",
                ["tag1", "tag2"]
            )

            db.session.commit()

            self.assertItemsEqual(post.tag_names(), ["tag1", "tag2"])


class UrlPostRetrievalTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            self.assertEqual(db.session.query(Url).count(), 0)
            self.assertEqual(db.session.query(Tag).count(), 0)
            self.assertEqual(db.session.query(Post).count(), 0)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_retrieve_url_posts(self):
        with self.app.app_context():
            Url.create("http://www.example.com/page_1")
            Url.create("http://www.example.com/page_2")

            db.session.commit()

            Post.create("page 1 test 1", "http://www.example.com/page_1",
                        ["tag1", "tag2"])

            db.session.commit()

            # sleep for a while so that the next posting has a different
            # added_at datetime
            time.sleep(0.1)

            Post.create("page 1 test 2", "http://www.example.com/page_1",
                        ["tag1", "tag3"])

            db.session.commit()

            posts = Url.get_posts("http://www.example.com/page_1")

            self.assertEqual(len(posts), 2)

            self.assertEqual(posts[0].title, "page 1 test 2")
            self.assertEqual(posts[1].title, "page 1 test 1")


class PostPaginationTests(TestCase):
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

        with self.app.app_context():
            db.create_all()

            load_mock_posts(db)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.get_engine(self.app).dispose()

        try:
            os.remove(self.db_path)
        except:
            pass

    def test_get_latest_by_page(self):
        with self.app.app_context():
            paginator = Post.get_latest_by_page(page=1, per_page=2)

            self.assertEqual(len(paginator.items), 2)
            self.assertEqual(paginator.pages, 2)
            self.assertEqual(paginator.page, 1)

            self.assertEqual(paginator.items[0].title, "page 4")
            self.assertEqual(paginator.items[1].title, "page 3")

            self.assertFalse(paginator.has_prev)
            self.assertTrue(paginator.has_next)
            self.assertEqual(paginator.next_num, 2)


if __name__ == "__main__":
    main()
