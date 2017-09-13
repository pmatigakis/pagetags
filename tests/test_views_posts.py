from unittest import main

from common import PagetagsTestWithMockData


class FrontPageViewtests(PagetagsTestWithMockData):
    def test_front_page(self):
        self.login()

        response = self.client.get("/")

        self.assertIn("<a href=\"/logout\">Logout</a>", response.data)

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

        self.assertIn("<a href=\"/tag/tag1\">tag1</a>", response.data)
        self.assertIn("<a href=\"/tag/tag3\">tag3</a>", response.data)
        self.assertIn("<a href=\"/tag/tag4\">tag4</a>", response.data)
        self.assertIn("<a href=\"/tag/tag5\">tag5</a>", response.data)
        self.assertIn("<a href=\"/tag/tag2\">tag2</a>", response.data)

        self.assertIn("<a href=\"/?page=2\">Next</a>", response.data)
        self.assertNotIn("<a href=\"/?page=0\">Previous</a>", response.data)

        self.logout()

    def test_front_page_page_2(self):
        self.login()

        response = self.client.get("/?page=2")

        self.assertIn("<a href=\"/logout\">Logout</a>", response.data)

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

        self.assertIn("<a href=\"/tag/tag1\">tag1</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag3\">tag3</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag4\">tag4</a>", response.data)
        self.assertNotIn("<a href=\"/tag/tag5\">tag5</a>", response.data)
        self.assertIn("<a href=\"/tag/tag2\">tag2</a>", response.data)

        self.assertNotIn("<a href=\"/?page=2\">Next</a>", response.data)
        self.assertIn("<a href=\"/?page=1\">Previous</a>", response.data)

        self.logout()


if __name__ == "__main__":
    main()
