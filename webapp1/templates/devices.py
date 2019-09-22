from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.forms import TruckForm, DevicesForm
from webapp1.models import truck, db, User, company, Device
devices_blueprint = Blueprint(
	'devices',
	__name__,
	template_folder='../templates/devices',
	url_prefix="/devices"
	)


@devices_blueprint.route('/createdevice', methods = ['GET', 'POST'])
def createdevice():
	form = DevicesForm(request.form)

	_update_ = (request.args.get('update'))
	if(_update_=='true'):
		flash('Device added.')
	Device_IP = request.form.get('Device_Number')
	Device_Name = request.form.get('devicename')
	_device_ = Device(uid = Device_Name, Device_Number = Device_IP, devicename = Device_Name)
	db.session.add(_device_)
	db.session.commit()

	return render_template('createdevice.html', form=form, role = 1)


@devices_blueprint.route('/show-device', methods = ['GET', 'POST'])
def showdevice():
	# usercompany = db.session.query(User.companyid).filter_by(id=current_user.get_id()).all()
	usercompany = db.session.query(company.uid).filter_by(user_id =1).all()
	print(usercompany)
	data = Device.query.all()
	print(data)
	try:
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
	except Exception as e:
		print(e)
	return render_template('showdevice.html', data = data, role = 2)


@devices_blueprint.route('/editdevice', methods = ['GET', 'POST'])
def editdevice():
	_device_to_edit_ = request.args.get('uid')
	_updated_ = (request.args.get('update'))
	_data_ = Device.query.filter_by(uid=_device_to_edit_).all()
	if (_updated_ == 'true'):
		flash('Record Updated.')
		#_data_[0].uid = request.form.get('Device_Number')
		_data_[0].Device_Number = request.form.get('Device_Number')
		_data_[0].devicename = request.form.get('devicename')
		db.session.add(_data_[0])
		db.session.commit()


	form = DevicesForm(request.form, obj=_data_[0])
	form.populate_obj(_data_[0])
	return render_template('editdevice.html', data = _data_[0], form = form)


@devices_blueprint.route('/deletedevice', methods = ['GET', 'POST'])
def deletedevice():
	_device_to_edit_ = request.args.get('uid')
	_updated_ = (request.args.get('update'))
	_data_ = Device.query.filter_by(uid=_device_to_edit_).all()
	 Device.query.filter_by(uid=_data_[0].uid).delete()
	if (_updated_ == 'true'):
		flash('Record Updated.')
		#_data_[0].uid = request.form.get('Device_Number')
		_data_[0].Device_Number = request.form.get('Device_Number')
		_data_[0].devicename = request.form.get('devicename')
		db.session.add(_data_[0])
		db.session.commit()


	form = DevicesForm(request.form, obj=_data_[0])
	form.populate_obj(_data_[0])
	return render_template('editdevice.html', data = _data_[0], form = form)

