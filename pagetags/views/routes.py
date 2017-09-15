from pagetags.views import posts, tags, authentication, categories


def add_view_routes(app):
    app.add_url_rule("/", view_func=posts.index)
    app.add_url_rule("/tag/<name>", view_func=tags.tag)
    app.add_url_rule("/tags", view_func=tags.tags)
    app.add_url_rule(
        "/login", view_func=authentication.login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=authentication.logout)
    app.add_url_rule("/categories", view_func=categories.categories)
    app.add_url_rule("/category/<name>", view_func=categories.category)
