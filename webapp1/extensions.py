from flask import flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_oauth import OAuth
from flask_login import LoginManager, login_required
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api
from flask_celery import Celery

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))
from celery.backends.redis import RedisBackend
oid = OpenID()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
rest_api = Api()
principals = Principal()
celery = Celery()



@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


@oid.after_login
def create_or_login(resp):
    from .models import db, User
    username = resp.fullname or resp.nickname or resp.email

    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    return redirect(url_for('blog.home'))