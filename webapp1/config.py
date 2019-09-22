from flask import flash, redirect, url_for, session
from flask.ext.bcrypt import Bcrypt
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed
from flask.ext.restful import Api

bcrypt = Bcrypt()
oid = OpenID()
principals = Principal()

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'


class ProdConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/elogstation1'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/elogstation'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/elogstation10'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database3.db'


    #SQLALCHEMY_DATABASE_URI = 'sqlite:///../database9.db'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_BACKEND_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
    import datetime


    CELERYBEAT_SCHEDULE = {
        'log-every-30-seconds': {
            'task': 'webapp1.tasks.log',
            'schedule': datetime.timedelta(seconds=5),
            'args': ("Message",)
        },
    }

    

# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///../database3.db'


login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

rest_api = Api()


@login_manager.user_loader
def load_user(userid):
    from models import User
    return User.query.get(userid)


@oid.after_login
def create_or_login(resp):
    from models import db, User
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
