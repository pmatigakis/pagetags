from unittest import main

from common import PagetagsTestWithMockData


class TagViewTests(PagetagsTestWithMockData):
    def test_view_tag(self):
        self.login()

        response = self.client.get("/tag/tag1")

        self.assertIn("<title>PageTags - Tag - tag1</title>", response.data)

        self.assertIn("post4", response.data)
        self.assertIn("post3", response.data)
        self.assertNotIn("post2", response.data)
        self.assertNotIn("post1>", response.data)
        self.assertNotIn("Previous", response.data)
        self.assertIn("Next", response.data)

        self.logout()

    def test_view_tag_page_2(self):
        self.login()

        response = self.client.get("/tag/tag1?page=2")

        self.assertIn("<title>PageTags - Tag - tag1</title>", response.data)
        self.assertIn("post1", response.data)
        self.assertIn("post2", response.data)
        self.assertNotIn("post3", response.data)
        self.assertNotIn("post4", response.data)
        self.assertIn("Previous", response.data)
        self.assertNotIn("Next", response.data)

        self.logout()

    def test_do_not_raise_an_error_if_tag_does_not_exist(self):
        self.login()

        response = self.client.get("/tag/tag444")

        self.assertIn("<p>This page doesn't exist</p>", response.data)

        self.logout()


class TagListViewTests(PagetagsTestWithMockData):
    def test_view_tags(self):
        self.login()

        response = self.client.get("/tags")

        self.assertIn("<title>PageTags - Tags</title>", response.data)

        self.assertIn("tag1", response.data)
        self.assertIn("tag2", response.data)
        self.assertNotIn("tag3", response.data)
        self.assertNotIn("Previous", response.data)
        self.assertIn("Next", response.data)

        self.logout()

    def test_view_tags_page_2(self):
        self.login()

        response = self.client.get("/tags?page=2")

        self.assertIn("<title>PageTags - Tags</title>", response.data)

        self.assertNotIn("tag1", response.data)
        self.assertNotIn("tag2", response.data)
        self.assertIn("tag3", response.data)
        self.assertIn("tag4", response.data)
        self.assertNotIn("tag5", response.data)
        self.assertIn(
            "<a href=\"/tags?page=1\">Previous</a>",
            response.data
        )

        self.assertIn(
            "<a href=\"/tags?page=3\">Next</a>",
            response.data
        )

        self.logout()


if __name__ == "__main__":
    main()
