from argparse import ArgumentTypeError

from pagetags.models import Post, Url


def post_title(title):
    """Post title argument type

    :param str title: the post title
    :rtype: str
    :returns: the post title
    """
    title = title.strip()

    if len(title) == 0:
        raise ArgumentTypeError("A title is required")
    elif len(title) > Post.TITLE_LENGTH:
        raise ArgumentTypeError("The title length is over the maximum allowed")

    return title


def post_url(url):
    """Post url argument type

    :param str url: the post url
    :rtype: str
    :returns: the post url
    """
    url = url.strip()

    if len(url) == 0:
        raise ArgumentTypeError("A url is required")
    elif len(url) > Url.URL_LENGTH:
        raise ArgumentTypeError("The url length is over the maximum allowed")

    return url
