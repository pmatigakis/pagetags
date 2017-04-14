from unittest import main

from common import PagetagsTestWithMockData


class AdminPageViewtests(PagetagsTestWithMockData):
    def test_cannot_access_admin_page_when_not_logged_in(self):
        with self.app.app_context():
            response = self.client.get("/admin", follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertIn("<title>PageTags - Login</title>", response.data)

    def test_admin_page_is_accessible_when_logged_in(self):
        with self.app.app_context():
            response = self.client.get("/admin", follow_redirects=True)

            self.login()

            response = self.client.get("/admin", follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertIn("<title>Home - admin</title>", response.data)


if __name__ == "__main__":
    main()
