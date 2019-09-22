from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed
from webapp1.forms import DriverForm
from flask import flash
from webapp1.models import truck, db, User, company, drivers
#TEST


drivers_blueprint = Blueprint(
	'driver',
	__name__,
	template_folder='../templates/drivers',
	url_prefix="/drivers"
	)


@drivers_blueprint.route('/create-driver', methods = ['GET', 'POST'])
def createdriver():
    form = DriverForm(request.form)
    #usercompany = db.session.query(company.uid).filter_by(user_id=current_user.get_id().all()

    if request.method == 'POST' and form.validate():
        firstname = request.form.get('First_Name')
        lastname = request.form.get('Last_Name')
        driverslicense = request.form.get('Drivers_License')
        driverslicensestate = request.form.get('Drivers_License_State')
        driver = drivers(First_Name=firstname, Last_Name=lastname, Drivers_License=driverslicense,
                         Drivers_License_State=driverslicensestate, user_id = current_user.get_id())
        db.session.add(driver)
        db.session.commit()
        flash('Driver Saved.')


    return render_template('create-driver.html', form=form)


@drivers_blueprint.route('/show-driver', methods = ['GET', 'POST'])
def showdriver():
    data = drivers.query.filter_by(user_id = current_user.get_id()).all()
    return render_template('showdriver.html', data=data)


@drivers_blueprint.route('/edit-driver', methods = ['GET', 'POST'])
def editdriver():
    _driver_to_edit_ = request.args.get('uid')
    _updated_ = (request.args.get('update'))
    _data_ = drivers.query.filter_by(uid=_driver_to_edit_).all()
    if(_updated_ == 'true'):
        flash('Record Updated.')
        _data_[0].First_Name = request.form.get('First_Name')
        _data_[0].Last_Name = request.form.get('Last_Name')
        _data_[0].Drivers_License = request.form.get('Drivers_License')
        _data_[0].Drivers_License_State = request.form.get('Drivers_License_State')


        db.session.add(_data_[0])
        db.session.commit()
    form = DriverForm(request.form, obj=_data_[0])

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
    flash_errors(form)

    form.populate_obj(_data_[0])
    return render_template('editdriver.html', data=_data_[0], form = form)


@drivers_blueprint.route('/deletedriver', methods = ['GET', 'POST'])
def deletedriver():
    try:
        _driver_to_edit_ = request.args.get('uid')
        _updated_ = (request.args.get('update'))
        _data_ = drivers.query.filter_by(uid=_driver_to_edit_, user_id = current_user.get_id()).delete()
        db.session.commit()
    except Exception as e:
        print(e)

    data = drivers.query.filter_by(user_id = current_user.get_id()).all()
    return render_template('showdriver.html', data=data)