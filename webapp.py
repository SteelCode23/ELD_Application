#This is the main application file

from flask import Flask
from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
import os
from wtforms.validators import AnyOf
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_mail import Message, Mail
from wtforms import form, fields, validators
import flask_admin as admin
import bcrypt
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual,DateTimeBetweenFilter, DateBetweenFilter, DateEqualFilter, DateTimeEqualFilter
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

try:
	# from webapp.models import db, User
	# from webapp.extensions import bcrypt, oid, login_manager, principals, rest_api, celery
	# from webapp1.controllers.account import account_blueprint
	# from webapp1.controllers.drivers import drivers_blueprint
	# from webapp1.controllers.dvir import dvir_blueprint
	# from webapp1.controllers.logs import logs_blueprint
	# from webapp1.controllers.trucks import trucks_blueprint
	from webapp1.controllers.elogstation import elogstation_blueprint
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
from webapp1.models import db  
from webapp1.controllers.account import account_blueprint
from webapp1.models import db, User, RPM,  DVIR, Role, RPM, company
from webapp1.extensions import bcrypt, oid, login_manager, principals, rest_api
from webapp1.controllers.account import account_blueprint
from webapp1.controllers.drivers import drivers_blueprint
from webapp1.controllers.maps import map_blueprint
from webapp1.controllers.dvir import dvir_blueprint
from webapp1.controllers.devices import devices_blueprint
from webapp1.controllers.logs import logs_blueprint
from webapp1.controllers.trucks import trucks_blueprint
from webapp1.controllers.elogstation import elogstation_blueprint
from webapp1.controllers.rest.eld import ELDAPI
from webapp1.controllers.rest.get_location import GetLocationsAPI
from webapp1.controllers.rest.status import StatusAPI
from webapp1.controllers.rest.events import EventsAPI
from webapp1.controllers.rest.certify import CertifyAPI
from webapp1.controllers.rest.post import PostAPI
from webapp1.controllers.rest.post_events import PostEventsAPI
from webapp1.controllers.webservices import webservices_blueprint
from webapp1.controllers.rest.auth import AuthApi
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed
from webapp1.extensions import poster_permission, admin_permission
from webapp1.forms import DriverForm, ElogForm, EmailServicesForm, BluetoothServicesForm, USBServicesForm, WIFIservicesForm
from webapp1.models import drivers, db, RPM, Device, Trailers, truck, Events, Events_Log, Events_Codes, Documents


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
    password = fields.PasswordField(validators=[validators.required()])
    email = fields.StringField()
    phone_number = fields.StringField()
    Company_Name = fields.StringField()
    Contact_Name = fields.StringField()
    Number_of_Trucks = fields.IntegerField()

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/test5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('webapp1.config.ProdConfig')

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)



class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

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

class MyGenericModelView(sqla.ModelView):
    can_export = True
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



class MyGenericModelViewCustomForm(sqla.ModelView):
    create_modal = True
    can_export = True
    list_template = 'list.html'
    column_filters = [
        DateEqualFilter(column=Events_Log.Event_Date, name='HOS Event Date'),
	DateBetweenFilter(column=Events_Log.Event_Date, name='HOS Event Date') ,
	DateTimeEqualFilter(column=Events_Log.Event_Date, name='HOS Event Date'),
	DateTimeBetweenFilter(column=Events_Log.Event_Date, name='HOS Event Date')
    ]

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
    #form_ajax_refs = {
    #    'Events_Codes': {
    #        'fields': (Events_Codes.name,)
    #    }
    #}

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    create_modal = True

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect('http://elogstation.com/elogstation/home')

        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return render_template('base.html', role = 2)
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()
        #return render_template('base.html', role = 2)
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
from webapp1.models import db

    #app.config.from_object('webapp1.config.DevConfig')
db.init_app(app)
try:
    db.create_all()
except Exception as e:
    print(e)

oid.init_app(app)
from flask_login import LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
init_login()


mail = Mail()
app.secret_key = 'development key'
mail.init_app(app)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'steel.ricciotti@gmail.com'
app.config["MAIL_PASSWORD"] = ''

mail.init_app(app)


#rest_api.init_app(app)
# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect('http://elogstation.com/elogstation/home')
        return redirect('http://elogstation.com/elogstation/home')

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect("/logs/showlogs")
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


# Create admin
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

admin = admin.Admin(app, 'Elogstation', index_view=MyAdminIndexView(), base_template='my_master.html')
#admin.add_view(ModelView(User, db.session))

# Flask views
@app.route('/')
def index():
    return redirect('http://elogstation.com/elogstation/home')



@app.route('/test1')
def createdriver():
    try:
        form = DriverForm(request.form)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('logs_blueprint/create-driver.html', form=form)




app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:postgres@localhost/ELOGSTATION_LOCALHOST'
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///../database10.db'
app.secret_key = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

db.init_app(app)
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(e)
bcrypt.init_app(app)
oid.init_app(app)
login_manager.init_app(app)
principals.init_app(app)
import flask_admin as admin1
admin = admin1.Admin(app, 'Elogstation', index_view=MyAdminIndexView())
# Add view
admin.add_view(MyModelView(User, db.session))
app.register_blueprint(account_blueprint)
app.register_blueprint(drivers_blueprint)
app.register_blueprint(dvir_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(trucks_blueprint)
app.register_blueprint(elogstation_blueprint)
app.register_blueprint(webservices_blueprint)
app.register_blueprint(map_blueprint)
rest_api.add_resource(ELDAPI, '/api/eld')
rest_api.add_resource(EventsAPI, '/api/events')
rest_api.add_resource(StatusAPI, '/api/status')
rest_api.add_resource(AuthApi, '/api/auth')
rest_api.add_resource(PostAPI, '/api/post')
rest_api.add_resource(PostEventsAPI, '/api/post_events')
rest_api.add_resource(GetLocationsAPI, '/api/get_location')
rest_api.add_resource(CertifyAPI, '/api/certify')
app.run(debug=True)
