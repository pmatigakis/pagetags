from pagetags.api.resources.posts import PostsResource, PostResource
from pagetags.api.resources.urls import UrlResource
from pagetags.api.resources.tags import TagsResource, TagPostsResource
from pagetags.api.resources.categories import (
    CategoryPostsResource, CategoriesResource
)


def add_api_routes(api):
    api.add_resource(TagsResource, "/api/v1/tags")
    api.add_resource(TagPostsResource, "/api/v1/tag/<tag>")
    api.add_resource(PostsResource, "/api/v1/posts")
    api.add_resource(UrlResource, "/api/v1/url")
    api.add_resource(PostResource, "/api/v1/post/<int:post_id>")
    api.add_resource(CategoryPostsResource, "/api/v1/category/<category>")
    api.add_resource(CategoriesResource, "/api/v1/categories")
