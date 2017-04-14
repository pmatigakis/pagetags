from flask_login import login_required, login_user, logout_user, current_user
from flask import current_app, render_template, redirect, url_for, flash

from pagetags import models, forms


def login():
    form = forms.Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        current_app.logger.info(u"authenticating user {}".format(username))

        user = models.User.authenticate(username, password)

        if user:
            current_app.logger.info(u"user {} authenticated".format(username))
            login_user(user)

            return redirect(url_for("index"))
        else:
            msg = u"user {} failed to authenticate"
            current_app.logger.warning(msg.format(username))
            flash("invalid username or password")

    return render_template("login.html", form=form)


@login_required
def logout():
    msg = u"logging out user {}"
    current_app.logger.info(msg.format(current_user.username))

    logout_user()

    return redirect(url_for("login"))
