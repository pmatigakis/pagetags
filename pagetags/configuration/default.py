import logging


PROPAGATE_EXCEPTIONS = True

ENABLE_LOGGING = False

LOG_FILE = "pagetags.log"
LOG_LEVEL = logging.INFO
LOG_FILE_SIZE = 10000000
LOG_FILE_COUNT = 5

FRONT_PAGE_ITEM_COUNT = 10
TAG_POSTS_PER_PAGE = 10
TAGS_PER_PAGE = 10

ERROR_404_HELP = False

# exp has been removed because we want to be able to create tokens without
# expiration data
JWT_REQUIRED_CLAIMS = ['iat', 'nbf']
