import flask
import flask_login
from flask import current_app as app
from flask_login import current_user, login_required

import feedi.models as models
from feedi.models import db


def init():
    login_manager = flask_login.LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))


@app.get("/auth/login")
def login():
    # if config has a default user it means auth is disabled
    # just load the user so we know what to point feeds to in the DB
    default_email = app.config.get('DEFAULT_AUTH_USER')
    if default_email:
        app.logger.debug("Logging default user %s", default_email)
        user = db.session.scalar(db.select(models.User).filter_by(email=default_email))
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('entry_list'))

    return flask.render_template('login.html')


@app.post('/auth/login')
def login_post():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    if not email or not password:
        return flask.render_template('login.html', error_msg="missing required field")

    user = db.session.scalar(db.select(models.User).filter_by(email=email))

    if not user or not user.check_password(password):
        return flask.render_template('login.html', error_msg="authentication failed")

    flask_login.login_user(user, remember=True)

    return flask.redirect(flask.url_for('entry_list'))


@app.get("/auth/kindle")
@login_required
def kindle_add():
    verifier, url = models.KindleDevice.signin_url()
    return flask.render_template('kindle.html', signin_url=url, verifier=verifier)


@app.post("/auth/kindle")
@login_required
def kindle_add_submit():
    verifier = flask.request.form.get('verifier')
    redirect_url = flask.request.form.get('redirect_url')
    models.KindleDevice.add_from_url(current_user.id, verifier, redirect_url)
    db.session.commit()
    return flask.redirect(flask.url_for('entry_list'))
