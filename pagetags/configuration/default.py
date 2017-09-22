PROPAGATE_EXCEPTIONS = True

FRONT_PAGE_ITEM_COUNT = 10
TAG_POSTS_PER_PAGE = 10

ERROR_404_HELP = False

# exp has been removed because we want to be able to create tokens without
# expiration data
JWT_REQUIRED_CLAIMS = ['iat', 'nbf']
