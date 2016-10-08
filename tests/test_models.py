from unittest import main

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from werkzeug.security import check_password_hash
from pagetags.models import User, Tag, Post, Url
from pagetags import db

from common import PagetagsTest, PagetagsTestWithMockData


class UserCreationModelTests(PagetagsTest):
    def test_create_user(self):
        with self.app.app_context():
            user = User.create("user1", "password")

            self.assertIsNone(user.id)
            self.assertEqual(user.username, "user1")
            self.assertTrue(check_password_hash(user.password, "password"))
            self.assertIsNotNone(user.jti)

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(user.id)

    def test_fail_to_create_user_using_existing_username(self):
        with self.app.app_context():
            User.create("user1", "password")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            User.create("user1", "password")

            self.assertRaises(IntegrityError, db.session.commit)


class UserRetrievalTests(PagetagsTestWithMockData):
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


class UserDeletionTests(PagetagsTestWithMockData):
    def test_delete_user(self):
        with self.app.app_context():
            user = User.delete("user1")

            self.assertIsNotNone(user)
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "user1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertEqual(db.session.query(User).count(), 0)


class UserPasswordTests(PagetagsTestWithMockData):
    def test_change_user_password(self):
        with self.app.app_context():
            user = User.get_by_username("user1")

            user.change_password("password1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            user = User.get_by_username("user1")

            self.assertTrue(check_password_hash(user.password, "password1"))


class UserAuthenticationTests(PagetagsTestWithMockData):
    def test_authenticate(self):
        with self.app.app_context():
            self.assertTrue(User.authenticate("user1", "password"))

    def test_fail_to_authenticate_with_invalid_password(self):
        with self.app.app_context():
            self.assertFalse(User.authenticate("user1", "password1"))

    def test_fail_to_authenticate_unknown_user(self):
        with self.app.app_context():
            self.assertFalse(User.authenticate("user2", "password"))

    def test_authenticate_using_jti(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(
                self.test_user_id, self.test_user_jti)

            self.assertIsNotNone(user)
            self.assertEqual(user.id, self.test_user_id)
            self.assertEqual(user.jti, self.test_user_jti)

    def test_fail_to_authenticate_using_invalid_jti(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(
                self.test_user_id, "invalid-jti")

            self.assertIsNone(user)

    def test_fail_to_authenticate_using_invalid_user_id(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(1234, self.test_user_jti)

            self.assertIsNone(user)


class TagCreationTests(PagetagsTest):
    def test_create_tag(self):
        with self.app.app_context():
            tag = Tag.create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNone(tag.id)
            self.assertEqual(tag.name, "tag1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(tag.id)

    def test_fail_to_create_duplicate_tag(self):
        with self.app.app_context():
            Tag.create("tag1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            Tag.create("tag1")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_tag(self):
        with self.app.app_context():
            tag = Tag.get_or_create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNone(tag.id)
            self.assertEqual(tag.name, "tag1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(tag.id)

    def test_get_or_create_existing_tag(self):
        with self.app.app_context():
            Tag.create("tag1")

            db.session.commit()

            tag = Tag.get_or_create("tag1")

            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.id)
            self.assertEqual(tag.name, "tag1")


class UrlCreationTests(PagetagsTest):
    def test_create_url(self):
        with self.app.app_context():
            url = Url.create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(url.id)

    def test_fail_to_create_duplicate_url(self):
        with self.app.app_context():
            Url.create("http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            Url.create("http://www.example.com")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_url(self):
        with self.app.app_context():
            url = Url.get_or_create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(url.id)

    def test_get_or_create_existing_url(self):
        with self.app.app_context():
            Url.create("http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            url = Url.get_or_create("http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNotNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

    def test_fail_to_create_url_with_empty_url_field(self):
        with self.app.app_context():
            self.assertRaises(ValueError, Url.create, "")

    def test_fail_to_create_url_with_very_large_url_field(self):
        large_url = "http://%s.com" % ("a" * Url.URL_LENGTH)

        with self.app.app_context():
            self.assertRaises(ValueError, Url.create, large_url)


class PostCreationTests(PagetagsTest):
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

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertIsNotNone(post.id)

    def test_post_name_tags(self):
        with self.app.app_context():
            post = Post.create(
                "post title",
                "http://www.example.com",
                ["tag1", "tag2"]
            )

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            self.assertItemsEqual(post.tag_names(), ["tag1", "tag2"])

    def test_fail_to_create_post_with_empty_title(self):
        with self.app.app_context():
            self.assertRaises(
                ValueError,
                Post.create,
                "",
                "http://www.google.com",
                ["tag1", "tag2"]
            )

    def test_fail_to_create_post_with_large_title_field(self):
        large_title = "a" * (Post.TITLE_LENGTH + 1)

        with self.app.app_context():
            self.assertRaises(
                ValueError,
                Post.create,
                large_title,
                "http://www.google.com",
                ["tag1", "tag2"]
            )


class UrlPostRetrievalTests(PagetagsTestWithMockData):
    def test_retrieve_url_posts(self):
        with self.app.app_context():
            posts = Url.get_posts("http://www.example.com/page_1")

            self.assertEqual(len(posts), 3)

            self.assertEqual(posts[0].title, "post3")
            self.assertEqual(posts[1].title, "post2")
            self.assertEqual(posts[2].title, "post1")

    def test_retrieve_url_posts_by_page(self):
        with self.app.app_context():
            url = Url.get_by_url("http://www.example.com/page_1")

            paginator = url.get_posts_by_page(1, per_page=2)

            self.assertEqual(len(paginator.items), 2)

            self.assertEqual(paginator.items[0].title, "post3")
            self.assertEqual(paginator.items[1].title, "post2")

    def test_retrieve_second_page_of_url_posts(self):
        with self.app.app_context():
            url = Url.get_by_url("http://www.example.com/page_1")

            paginator = url.get_posts_by_page(2, per_page=2)

            self.assertEqual(len(paginator.items), 1)

            self.assertEqual(paginator.items[0].title, "post1")


class PostPaginationTests(PagetagsTestWithMockData):
    def test_get_latest_by_page(self):
        with self.app.app_context():
            paginator = Post.get_latest_by_page(page=1, per_page=2)

            self.assertEqual(len(paginator.items), 2)
            self.assertEqual(paginator.pages, 2)
            self.assertEqual(paginator.page, 1)

            self.assertEqual(paginator.items[0].title, "post4")
            self.assertEqual(paginator.items[1].title, "post3")

            self.assertFalse(paginator.has_prev)
            self.assertTrue(paginator.has_next)
            self.assertEqual(paginator.next_num, 2)


if __name__ == "__main__":
    main()
