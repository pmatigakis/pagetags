from unittest import main

from common import PagetagsTestWithMockData


class FrontPageViewtests(PagetagsTestWithMockData):
    def test_front_page(self):
        self.login()

        response = self.client.get("/")

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

        self.assertIn("tag1", response.data)
        self.assertIn("tag3", response.data)
        self.assertIn("tag4", response.data)
        self.assertIn("tag5", response.data)
        self.assertIn("tag2", response.data)

        self.assertIn("Next", response.data)
        self.assertIn("/?page=2", response.data)
        self.assertNotIn("Previous", response.data)

        self.logout()

    def test_front_page_page_2(self):
        self.login()

        response = self.client.get("/?page=2")

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

        self.assertIn("tag1", response.data)
        self.assertNotIn("tag3", response.data)
        self.assertNotIn("tag4", response.data)
        self.assertNotIn("tag5", response.data)
        self.assertIn("tag2", response.data)

        self.assertNotIn("Next", response.data)
        self.assertIn("Previous", response.data)
        self.assertIn("/?page=1", response.data)

        self.logout()


if __name__ == "__main__":
    main()
