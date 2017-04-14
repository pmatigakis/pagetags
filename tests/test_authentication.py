from unittest import main, TestCase

import arrow

from pagetags.models import User
from pagetags.authentication import payload_handler, create_token_payload

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


class TokenPayloadCreationTests(TestCase):
    def test_create_token_payload_without_expiration_date(self):
        user_id = 123
        jti = "abcd"

        payload = create_token_payload(user_id, jti)

        self.assertIsInstance(payload, dict)
        self.assertIn("iat", payload)
        self.assertIn("nbf", payload)
        self.assertIsInstance(payload["iat"], int)
        self.assertIsInstance(payload["nbf"], int)

        iat = payload["iat"]
        nbf = payload["nbf"]

        self.assertEqual(iat, nbf)

        self.assertDictEqual(
            payload,
            {
                "iat": iat,
                "nbf": nbf,
                "identity": user_id,
                "jti": jti
            }
        )

    def test_create_token_payload_with_expiration_date(self):
        user_id = 123
        jti = "abcd"
        expiration_time = arrow.utcnow().replace(days=1)

        payload = create_token_payload(
            user_id=user_id,
            jti=jti,
            expires_at=expiration_time.strftime("%Y/%m/%d %H:%M:%S")
        )

        self.assertIsInstance(payload, dict)
        self.assertIn("iat", payload)
        self.assertIn("nbf", payload)
        self.assertIn("exp", payload)
        self.assertIsInstance(payload["iat"], int)
        self.assertIsInstance(payload["nbf"], int)
        self.assertIsInstance(payload["exp"], int)

        iat = payload["iat"]
        nbf = payload["nbf"]

        self.assertEqual(iat, nbf)
        self.assertGreater(payload["exp"], iat)

        self.assertDictEqual(
            payload,
            {
                "iat": iat,
                "nbf": nbf,
                "identity": user_id,
                "jti": jti,
                "exp": expiration_time.timestamp
            }
        )


if __name__ == "__main__":
    main()
