from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
import odb


elogstation_blueprint = Blueprint(
	'odb',
	__name__,
	template_folder='../templates/elogstation',
	url_prefix="/elogstation"
	)


@login_required
@elogstation_blueprint.route('/')
@elogstation_blueprint.route('/<int:page>')
def home(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('.login_view'))
    return render_template('home.html', page = page)


@login_required
@elogstation_blueprint.route('/home')
def landingpage(page=1):
    return render_template('landingpage.html', page = page)

@elogstation_blueprint.route('/register')
def register():
    return render_template('elogstationexample.html')



@elogstation_blueprint.route('/register2')
def register2():
    return render_template(
        'register2.html'
    )

