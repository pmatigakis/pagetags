from unittest import main

from common import PagetagsTestsWithUser


class LoginTests(PagetagsTestsWithUser):
    def test_login(self):
        client = self.app.test_client()

        request_data = {
            "username": self.test_user_username,
            "password": self.test_user_password
        }

        response = self.client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = client.post("/login",
                               data=request_data,
                               follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)

    def test_login_then_logout(self):
        request_data = {
            "username": self.test_user_username,
            "password": self.test_user_password
        }

        response = self.client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = self.client.post("/login",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("<title>PageTags</title>", response.data)

        response = self.client.get("/logout", follow_redirects=True)

        self.assertIn("<title>PageTags - Login</title>", response.data)

    def test_fail_to_login_with_invalid_password(self):
        request_data = {
            "username": self.test_user_username,
            "password": "12345678"
        }

        response = self.client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = self.client.post("/login",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("invalid username or password", response.data)

    def test_fail_to_login_with_invalid_username(self):
        request_data = {
            "username": "abcdefg",
            "password": self.test_user_password
        }

        response = self.client.get("/login", follow_redirects=True)

        self.assertIn("PageTags - Login", response.data)

        response = self.client.post("/login",
                                    data=request_data,
                                    follow_redirects=True)

        self.assertIn("invalid username or password", response.data)


if __name__ == "__main__":
    main()
