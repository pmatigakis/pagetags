from unittest import TestCase, main
from argparse import ArgumentTypeError

from pagetags import argtypes
from pagetags.models import Post, Url


class PostTitleTests(TestCase):
    def test_post_title(self):
        title = argtypes.post_title("post title")

        self.assertEqual(title, "post title")

    def test_raise_error_on_empty_post_title(self):
        self.assertRaises(ArgumentTypeError, argtypes.post_title, "")

    def test_raise_error_on_very_large_post_title(self):
        large_post_title = "a" * (Post.TITLE_LENGTH + 1)

        self.assertRaises(
            ArgumentTypeError, argtypes.post_title, large_post_title)


class PostUrlTests(TestCase):
    def test_post_url(self):
        url = argtypes.post_url("http://www.example.com")

        self.assertEqual(url, "http://www.example.com")

    def test_raise_error_on_empty_post_url(self):
        self.assertRaises(ArgumentTypeError, argtypes.post_url, "")

    def test_raise_error_on_very_large_post_url(self):
        large_post_url = "http://%s.com" % ("a" * Url.URL_LENGTH)

        self.assertRaises(
            ArgumentTypeError, argtypes.post_title, large_post_url)


if __name__ == "__main__":
    main()
