from flask import Flask
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed, RoleNeed
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
try:
	from webapp.models import db, User
	from webapp.extensions import bcrypt, oid, login_manager, principals, rest_api, celery
	from webapp.controllers.account import account_blueprint
	from webapp.controllers.drivers import drivers_blueprint
	from webapp.controllers.dvir import dvir_blueprint
	from webapp.controllers.logs import logs_blueprint
	from webapp.controllers.trucks import trucks_blueprint
	from webapp.controllers.elogstation import elogstation_blueprint
except Exception as e:
	try:
		from models import db, User
		from extensions import bcrypt, oid, login_manager, principals, rest_api, celery
		from controllers.account import account_blueprint
		from webapp.controllers.drivers import drivers_blueprint
		from .controllers.dvir import dvir_blueprint
		from controllers.logs import logs_blueprint
		from controllers.trucks import trucks_blueprint
		from controllers.elogstation import elogstation_blueprint
	except Exception as e:
		print(e)

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config.ProdConfig')

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
# class MyModelView(sqla.ModelView):
#
#     def is_accessible(self):
#         return login.current_user.is_authenticated
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if login.current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect('http://localhost:5000/elogstation/home')
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return render_template("")
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
# Initialize flask-login
init_login()
def create_app(object_name):
    """


    """
    from models import db
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../databasetest.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('config.ProdConfig')
    db.init_app(app)
    db.create_all()
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    celery.init_app(app)
    # Create admin
    import flask_admin as admin1
    admin = admin1.Admin(app, 'Elogstation', index_view=MyAdminIndexView())
    # Add view
    admin.add_view(MyModelView(User, db.session))
    return app



if __name__ == '__main__':
	# try:
	# 	app = create_app('config.ProdConfig')
	# except Exception as e:
	app = create_app('config.ProdConfig')
	app.run(debug=True, port = 5054)
