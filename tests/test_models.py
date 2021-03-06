from unittest import main

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash
from flask_sqlalchemy import Pagination

from pagetags.models import User, Tag, Post, Url, Category, PostCategory
from pagetags import db

from common import PagetagsTest, PagetagsTestWithMockData


class UserCreationModelTests(PagetagsTest):
    def test_create_user(self):
        with self.app.app_context():
            user = User.create(db.session, "user1", "password")

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
            User.create(db.session, "user1", "password")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            User.create(db.session, "user1", "password")

            self.assertRaises(IntegrityError, db.session.commit)


class UserRetrievalTests(PagetagsTestWithMockData):
    def test_get_user_by_username(self):
        with self.app.app_context():
            user = User.get_by_username(db.session, "user1")

            self.assertIsNotNone(user)
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "user1")
            self.assertTrue(check_password_hash(user.password, "password"))

    def test_fail_to_get_user_that_doesnt_exist(self):
        with self.app.app_context():
            user = User.get_by_username(db.session, "user2")

            self.assertIsNone(user)


class UserDeletionTests(PagetagsTestWithMockData):
    def test_delete_user(self):
        with self.app.app_context():
            user = User.delete(db.session, "user1")

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
            user = User.get_by_username(db.session, "user1")

            user.change_password("password1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            user = User.get_by_username(db.session, "user1")

            self.assertTrue(check_password_hash(user.password, "password1"))


class UserAuthenticationTests(PagetagsTestWithMockData):
    def test_authenticate(self):
        with self.app.app_context():
            self.assertTrue(User.authenticate(db.session, "user1", "password"))

    def test_fail_to_authenticate_with_invalid_password(self):
        with self.app.app_context():
            self.assertFalse(
                User.authenticate(db.session, "user1", "password1"))

    def test_fail_to_authenticate_unknown_user(self):
        with self.app.app_context():
            self.assertFalse(
                User.authenticate(db.session, "user2", "password"))

    def test_authenticate_using_jti(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(
                db.session, self.test_user_id, self.test_user_jti)

            self.assertIsNotNone(user)
            self.assertEqual(user.id, self.test_user_id)
            self.assertEqual(user.jti, self.test_user_jti)

    def test_fail_to_authenticate_using_invalid_jti(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(
                db.session, self.test_user_id, "invalid-jti")

            self.assertIsNone(user)

    def test_fail_to_authenticate_using_invalid_user_id(self):
        with self.app.app_context():
            user = User.authenticate_using_jti(
                db.session, 1234, self.test_user_jti)

            self.assertIsNone(user)


class TagCreationTests(PagetagsTest):
    def test_create_tag(self):
        with self.app.app_context():
            tag = Tag.create(db.session, "tag1")

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
            Tag.create(db.session, "tag1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            Tag.create(db.session, "tag1")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_tag(self):
        with self.app.app_context():
            tag = Tag.get_or_create(db.session, "tag1")

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
            Tag.create(db.session, "tag1")

            db.session.commit()

            tag = Tag.get_or_create(db.session, "tag1")

            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.id)
            self.assertEqual(tag.name, "tag1")


class UrlCreationTests(PagetagsTest):
    def test_create_url(self):
        with self.app.app_context():
            url = Url.create(db.session, "http://www.example.com")

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
            Url.create(db.session, "http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            Url.create(db.session, "http://www.example.com")

            self.assertRaises(IntegrityError, db.session.commit)

    def test_get_or_create_new_url(self):
        with self.app.app_context():
            url = Url.get_or_create(db.session, "http://www.example.com")

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
            Url.create(db.session, "http://www.example.com")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to commit transaction")

            url = Url.get_or_create(db.session, "http://www.example.com")

            self.assertIsNotNone(url)
            self.assertIsNotNone(url.id)
            self.assertEqual(url.url, "http://www.example.com")

    def test_fail_to_create_url_with_empty_url_field(self):
        with self.app.app_context():
            self.assertRaises(ValueError, Url.create, db.session, "")

    def test_fail_to_create_url_with_very_large_url_field(self):
        large_url = "http://%s.com" % ("a" * Url.URL_LENGTH)

        with self.app.app_context():
            self.assertRaises(ValueError, Url.create, db.session, large_url)


class PostCreationTests(PagetagsTest):
    def test_create_posting(self):
        with self.app.app_context():
            post = Post.create(
                db.session,
                "post title",
                "http://www.example.com",
                ["tag1", "tag2"],
                ["category_1"]
            )

            self.assertIsNotNone(post)
            self.assertIsNone(post.id)
            self.assertEqual(post.title, "post title")
            self.assertEqual(post.url.url, "http://www.example.com")
            self.assertItemsEqual(
                [tag.name for tag in post.tags],
                ["tag1", "tag2"]
            )
            self.assertItemsEqual(
                [category_object.name for category_object in post.categories],
                ["category_1"]
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
                db.session,
                "post title",
                "http://www.example.com",
                ["tag1", "tag2"],
                ["category_1"]
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
                db.session,
                "",
                "http://www.google.com",
                ["tag1", "tag2"],
                ["category_1"]
            )

    def test_fail_to_create_post_with_large_title_field(self):
        large_title = "a" * (Post.TITLE_LENGTH + 1)

        with self.app.app_context():
            self.assertRaises(
                ValueError,
                Post.create,
                db.session,
                large_title,
                "http://www.google.com",
                ["tag1", "tag2"],
                ["category_1"]
            )


class UrlPostRetrievalTests(PagetagsTestWithMockData):
    def test_retrieve_url_posts(self):
        with self.app.app_context():
            posts = Url.get_posts(db.session, "http://www.example.com/page_1")

            self.assertEqual(len(posts), 3)

            self.assertEqual(posts[0].title, "post3")
            self.assertEqual(posts[1].title, "post2")
            self.assertEqual(posts[2].title, "post1")

    def test_retrieve_url_posts_by_page(self):
        with self.app.app_context():
            url = Url.get_by_url(db.session, "http://www.example.com/page_1")

            paginator = url.get_posts_by_page(1, per_page=2)

            self.assertEqual(len(paginator.items), 2)

            self.assertEqual(paginator.items[0].title, "post3")
            self.assertEqual(paginator.items[1].title, "post2")

    def test_retrieve_second_page_of_url_posts(self):
        with self.app.app_context():
            url = Url.get_by_url(db.session, "http://www.example.com/page_1")

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


class TagTests(PagetagsTestWithMockData):
    def test_post_count(self):
        with self.app.app_context():
            tag = Tag.get_by_name(db.session, "tag2")

            self.assertEqual(tag.post_count(db.session), 2)

    def test_get_tags_by_page(self):
        with self.app.app_context():
            paginator = Tag.get_tags_by_page(page=1, per_page=2)

            self.assertIsInstance(paginator, Pagination)
            self.assertEqual(paginator.page, 1)
            self.assertEqual(paginator.per_page, 2)

            self.assertEqual(paginator.items[0].name, "tag1")
            self.assertEqual(paginator.items[1].name, "tag2")

            paginator = Tag.get_tags_by_page(page=2, per_page=2)

            self.assertEqual(paginator.page, 2)
            self.assertEqual(paginator.items[0].name, "tag3")
            self.assertEqual(paginator.items[1].name, "tag4")


class PostRetrievalTests(PagetagsTestWithMockData):
    def test_get_by_id(self):
        with self.app.app_context():
            post = Post.get_by_id(db.session, 1)

            self.assertIsNotNone(post)
            self.assertEqual(post.id, 1)
            self.assertEqual(post.title, "post1")
            self.assertEqual(post.url.url, "http://www.example.com/page_1")


class PostUpdateTests(PagetagsTestWithMockData):
    def test_update(self):
        with self.app.app_context():
            post = Post.get_by_id(db.session, 1)

            title = "new post1 title"
            url = "http://www.example_1.com/new_post1_url"
            tags = ["tag1000", "tag2000"]

            post.update(db.session, title, url, tags)

            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                self.fail("failed to update post")

            post = Post.get_by_id(db.session, 1)

            self.assertEqual(post.id, 1)
            self.assertEqual(post.title, title)
            self.assertEqual(post.url.url, url)
            self.assertItemsEqual([tag.name for tag in post.tags], tags)

    def test_change_the_category_of_a_post(self):
        with self.app.app_context():
            post = db.session.query(Post).get(1)
            category = db.session.query(Category).get(2)

            post.categories = [category]

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to update the post categories")

            post = db.session.query(Post).get(1)
            self.assertEqual(len(post.categories), 1)
            self.assertEqual(post.categories[0].name, "category_2")

    def test_change_the_category_of_a_post_using_post_cetegory_object(self):
        with self.app.app_context():
            post = db.session.query(Post).get(1)
            category = db.session.query(Category).get(2)

            PostCategory.create(db.session, post=post, category=category)

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to update the post categories")

            post = db.session.query(Post).get(1)
            self.assertEqual(len(post.categories), 1)
            self.assertEqual(post.categories[0].name, "category_2")


class CategoryTests(PagetagsTest):
    def test_create_category(self):
        with self.app.app_context():
            category = Category.create(db.session, "category_1")

            self.assertIsNone(category.id)

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to create category object")

            self.assertIsNotNone(category.id)

    def test_fail_to_create_categories_with_the_same_name(self):
        with self.app.app_context():
            Category.create(db.session, "category_1")

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to create category object")

            Category.create(db.session, "category_1")

            self.assertRaises(IntegrityError, db.session.commit)


class CategoryRetrievalTests(PagetagsTest):
    def setUp(self):
        super(CategoryRetrievalTests, self).setUp()

        with self.app.app_context():
            for i in range(10):
                Category.create(db.session, "category_{}".format(i))

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to load mock data")

    def get_by_page(self):
        with self.app.app_context():
            paginator = Category.get_by_page(page_num=1, per_page=3)

            self.assertIsNotNone(paginator)

            self.assertEqual(paginator.page, 1)
            self.assertEqual(paginator.per_page, 3)

            self.assertEqual(paginator.items[0].name, "category_9")
            self.assertEqual(paginator.items[-1].name, "category_7")

            paginator = Category.get_by_page(page_num=2, per_page=3)

            self.assertIsNotNone(paginator)

            self.assertEqual(paginator.page, 2)
            self.assertEqual(paginator.per_page, 3)

            self.assertEqual(paginator.items[0].name, "category_6")
            self.assertEqual(paginator.items[-1].name, "category_4")

            paginator = Category.get_by_page(page_num=4, per_page=3)

            self.assertIsNotNone(paginator)

            self.assertEqual(paginator.page, 4)
            self.assertEqual(paginator.per_page, 3)

            self.assertEqual(paginator.items[0].name, "category_0")
            self.assertEqual(len(paginator.items), 1)


class PostCategoryTests(PagetagsTestWithMockData):
    def test_create_post_category(self):
        with self.app.app_context():
            category = db.session.query(Category).get(1)
            post = db.session.query(Post).get(1)

            post_category = PostCategory.create(
                session=db.session,
                post=post,
                category=category
            )

            db.session.add(post_category)

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                self.fail("failed to create post category object")

            self.assertEqual(len(post.categories), 1)
            self.assertItemsEqual(
                ["category_1"],
                [
                    post_category_object.name
                    for post_category_object in post.categories
                ]
            )


if __name__ == "__main__":
    main()
