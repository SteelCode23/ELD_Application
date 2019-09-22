from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

account_blueprint = Blueprint(
	'account',
	__name__,
	template_folder='../templates/account',
	url_prefix="/account"
	)

@login_required
@account_blueprint.route('/')
@account_blueprint.route('/<int:page>')
def home(page=1):
    return render_template(
        'home.html', number = page
    )
