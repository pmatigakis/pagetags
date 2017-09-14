from unittest import main

from sqlalchemy.exc import SQLAlchemyError

from pagetags.models import db, Category

from common import PagetagsTest


class CategoriesViewTests(PagetagsTest):
    def setUp(self):
        super(CategoriesViewTests, self).setUp()

        with self.app.app_context():
            with self.app.app_context():
                for i in range(25):
                    Category.create("category_{}".format(i))

                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    self.fail("failed to load mock data")

    def test_get_categories(self):
        response = self.client.get("/categories")

        self.assertEqual(response.status_code, 200)

        self.assertIn("category_24", response.data)
        self.assertNotIn("category_0", response.data)

        self.assertIn("Next", response.data)
        self.assertNotIn("Previous", response.data)

    def test_get_categories_second_page(self):
        response = self.client.get("/categories", query_string={"page": 2})

        self.assertEqual(response.status_code, 200)

        self.assertNotIn("category_24", response.data)
        self.assertIn("category_14", response.data)
        self.assertNotIn("category_0", response.data)

        self.assertIn("Next", response.data)
        self.assertIn("Previous", response.data)

    def test_get_categories_last_page(self):
        response = self.client.get("/categories", query_string={"page": 3})

        self.assertEqual(response.status_code, 200)

        self.assertNotIn("category_24", response.data)
        self.assertNotIn("category_14", response.data)
        self.assertIn("category_0", response.data)

        self.assertNotIn("Next", response.data)
        self.assertIn("Previous", response.data)

    def test_fail_to_get_page_that_does_not_exist(self):
        response = self.client.get("/categories", query_string={"page": 10})

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    main()
