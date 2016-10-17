from unittest import main

from pagetags.models import User
from pagetags.authentication import payload_handler

from common import PagetagsTestWithMockData


class PayloadHandlerTests(PagetagsTestWithMockData):
    def test_payload_handler(self):
        user = User(id=1, username="user1", jti="abcde")

        with self.app.app_context():
            payload = payload_handler(user)

            self.assertIn("identity", payload)
            self.assertIn("jti", payload)

            self.assertEqual(payload["identity"], 1)
            self.assertEqual(payload["jti"], "abcde")


if __name__ == "__main__":
    main()
