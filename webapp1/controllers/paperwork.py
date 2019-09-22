from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

account_blueprint = Blueprint(
	'paperwork',
	__name__,
	template_folder='../templates/paperwork',
	url_prefix="/paperwork"
	)

@login_required
@paperwork_blueprint.route('/')
@paperwork_blueprint.route('/<int:page>')
def paperwork(page=1):
    return render_template(
        'home.html', number = page
    )
