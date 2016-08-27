import os
from unittest import TestCase, main

from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash
from pagetags.main import create_app
from pagetags.models import User, Tag, Posting, Url
from pagetags import db


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


class PostingCreationTests(TestCase):
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
            self.assertEqual(db.session.query(Posting).count(), 0)

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
            posting = Posting.create(
                "posting title",
                "http://www.example.com",
                ["tag1", "tag2"]
            )

            self.assertIsNotNone(posting)
            self.assertIsNone(posting.id)
            self.assertEqual(posting.title, "posting title")
            self.assertEqual(posting.url.url, "http://www.example.com")
            self.assertItemsEqual(
                [tag.name for tag in posting.tags],
                ["tag1", "tag2"]
            )

            db.session.commit()

            self.assertIsNotNone(posting.id)


if __name__ == "__main__":
    main()
