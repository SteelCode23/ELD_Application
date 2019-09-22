from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from flask import flash
from webapp1.forms import TruckForm
from webapp1.models import truck, db, User, company, Device, drivers
trucks_blueprint = Blueprint(
	'trucks',
	__name__,
	template_folder='../templates/trucks',
	url_prefix="/trucks"
	)


@trucks_blueprint.route('/login', methods = ['GET', 'POST'])
def Login():
	form = TruckForm(request.form)
	device = request.args.get('device')
	drivers_status = db.session.query(drivers.Current_Status).filter_by(user_id = current_user.get_id()).all()
	drivers_status = [i for i in drivers_status][0]
	#drivers_status = db.session.query(drivers.Current_Status).filter_by(uid=current_user.get_id()).all()
	#drivers_status = db.session.query(drivers.Current_Status).all()
	#drivers_status = drivers_status[0][0]
	#drivers_status = db.session.query(drivers.Current_Status).filter_by(uid=1).all()
	#All this does is returns the current users device
	try:
		mydevice = db.session.query(Device.Device_Number).filter_by(driver_id = current_user.get_id()).all()
		mydevice = mydevice[0][0]
	except Exception as e:
		mydevice = "Gas"
	#performs necessary transactions to update drivers state

	#if (data == 0):
	db.session.execute('update device set status = 1 where "Device_Number" = :device', {'device':device})
	db.session.commit()
	db.session.execute('update drivers set "Current_Status" = 1 where user_id = :user', {'user':current_user.get_id()})
	db.session.commit()
	db.session.execute('update drivers set "device_id" = :device where user_id = :driver', {'driver':current_user.get_id(), 'device':device})
	db.session.commit()
	db.session.execute('update device set driver_id = :driver where "Device_Number" = :device', {'device':device, 'driver':current_user.get_id()})
	db.session.commit()


	#ListOfLoggedIn = {'device':{'number':'name'},{'driver':'name'},{'status':'name'}}
	# ListOfLoggedIn = {}
	# device = db.session.query(Device.Device_Number, Device.driver_id, Device.status).all()
	# from collections import namedtuple
	# named_device = []
	# name_id_status = namedtuple("Name_ID_Status",["Device_Number","driver_id","status"])
	# for named_data in device:
	# 	namedPi = name_id_status(*named_data)
	# 	named_device.append(namedPi)


	device = db.session.query(Device.Device_Number, Device.driver_id, Device.status).all()
	

	from collections import namedtuple
	named_device = []
	name_id_status = namedtuple("Name_ID_Status",["Device_Number","driver_id","status"])
	for named_data in device:
		namedPi = name_id_status(*named_data)
		named_device.append(namedPi)


	for i in range(len(named_device)):
		if(named_device[i].driver_id != None):
			data = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = named_device[i].driver_id).all()
			try:
				named_device[i] = named_device[i]._replace(driver_id = data[0][0] + " " + data[0][1])
			except Exception as e:
				named_device[i] = named_device[i]._replace(driver_id ="John Doe")

	name__ = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = current_user.get_id()).all()
	name = name__[0][0] + " " + name__[0][1]

	return render_template('device_login.html', device = device, form = form, named_device = named_device,drivers_status = 1, drivers_name = name, mydevice = mydevice, role =2 )


@trucks_blueprint.route('/logout', methods = ['GET', 'POST'])
def Logout():
	form = TruckForm(request.form)
	device = request.args.get('device')
	drivers_status = db.session.query(drivers.Current_Status).filter_by(user_id = current_user.get_id()).all()
	data = [i for i in drivers_status][0]


	drivers_name_temp = db.session.query(drivers.First_Name).filter_by(user_id = current_user.get_id()).all()
	drivers_name = [i for i in drivers_name_temp][0]


	drivers_status = db.session.query(drivers.Current_Status).filter_by(uid=current_user.get_id()).all()
	drivers_status = [i for i in drivers_status[0]]


	db.session.execute('update device set status = 0 where "Device_Number" = :device', {'device':device})
	db.session.execute('update drivers set "Current_Status" = 0 where user_id = :device', {'device':current_user.get_id()})
	db.session.execute('update device set driver_id = 0 where "Device_Number" = :device', {'device':device})
	db.session.execute('update drivers set "device_id" = 0 where user_id = :user', {'user':current_user.get_id()})
	db.session.commit()


	device = db.session.query(Device.Device_Number, Device.driver_id, Device.status).all()
	

	from collections import namedtuple
	named_device = []
	name_id_status = namedtuple("Name_ID_Status",["Device_Number","driver_id","status"])
	for named_data in device:
		namedPi = name_id_status(*named_data)
		named_device.append(namedPi)


	for i in range(len(named_device)):
		if(named_device[i].driver_id != None):
			data = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = named_device[i].driver_id).all()
			try:
				named_device[i] = named_device[i]._replace(driver_id = data[0][0] + " " + data[0][1])
			except Exception as e:
				named_device[i] = named_device[i]._replace(driver_id ="John Doe")

	name__ = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = current_user.get_id()).all()
	name = name__[0][0] + " " + name__[0][1]


	return render_template('device_login.html', device = device, form = form, named_device = named_device, drivers_status = 0, drivers_name = name)


@trucks_blueprint.route('/truckdetails', methods = ['GET', 'POST'])
def TruckDetails():
	form = TruckForm(request.form)
	_truck_list_ = db.session.query(truck.VIN, truck.License_Plate, truck.State_province, truck.unit).all()
	return render_template('showtruck.html', truck = _truck_list_ , form = form, role = 2)


@trucks_blueprint.route('/createtruck', methods = ['GET', 'POST'])
def createtruck():
	#Need to add flashes when data is created.
	form = TruckForm(request.form)
	if request.method == 'POST' and form.validate():
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
		thistruck = truck(unit=unit, License_Plate=LicensePlate, State_province=State_province, VIN=VIN, user_id = current_user.get_id())
		db.session.add(thistruck)
		db.session.commit()
		flash('Record Created.')

	return render_template('create-truck.html', form=form, role = 1)


##Having some trouble rendering a specific driver on a specific truck
@trucks_blueprint.route('/sign-in-to-truck', methods = ['GET', 'POST'])
def Sign_In():
	ListOfLoggedIn = {}
	form = TruckForm(request.form)
	drivers_status = db.session.query(drivers.Current_Status).filter_by(user_id = current_user.get_id()).all()
	my_device = db.session.query(Device.Device_Number).all()
	mydevice = [i for i in my_device][0]
	drivers_name_temp = db.session.query(drivers.First_Name).filter_by(user_id = current_user.get_id()).all()
	drivers_name = [i for i in drivers_name_temp][0]
	newdata = [i for i in drivers_status][0]
	device = db.session.query(Device.Device_Number, Device.driver_id).all()

	for i in device:
		#If a driver is assigned.
		if(i[1] != None):
			try:
				#Query that actual driver.
				data = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid=i[1]).all()
				#This literally just grabs first name and last name.
				name = data[0][0] + " " + data[0][1]
				ListOfLoggedIn[i[0]] = name
				print(name)
			except Exception as e:
				print(e)
				name = ""
		else:
			ListOfLoggedIn[i[0]] = "Not Logged In"

	db.session.execute('update drivers set "Current_Status" = 1 where user_id = :user', {'user':current_user.get_id()})
	db.session.commit()
	newdata = 1
	return render_template('device_login.html', device = device, form = form, ListOfLoggedIn = ListOfLoggedIn, drivers_status = 0, mydevice = mydevice, drivers_name = name, role = 2)


@trucks_blueprint.route('/showtruck', methods = ['GET', 'POST'])
def showtruck():
	data = truck.query.filter_by(user_id = current_user.get_id()).all()
	try:
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
	except Exception as e:
		print(e)
	return render_template('showtruck.html', data = data, role = 2)


@trucks_blueprint.route('/deletetruck', methods = ['GET', 'POST'])
def deletetruck():
	#data = truck.query.filter_by(user_id = current_user.get_id()).all()
	try:
		_truck_to_edit_ = (request.args.get('uid'))
		updated_ = (request.args.get('update'))
		data_ = truck.query.filter_by(uid=_truck_to_edit_).delete()
		db.session.commit()
	except Exception as e:
		print(e)
	data = truck.query.filter_by(user_id = current_user.get_id()).all()
	try:
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
	except Exception as e:
		print(e)
	return render_template('showtruck.html', data = data, role = 2)


@trucks_blueprint.route('/editruck', methods = ['GET', 'POST'])
def edittruck():
	_truck_to_edit_ = (request.args.get('uid'))
	_updated_ = (request.args.get('update'))
	_data_ = truck.query.filter_by(uid=_truck_to_edit_).all()
	if(_updated_ == 'true'):
		_data_[0].unit = request.form.get('unit')
		_data_[0].License_Plate = request.form.get('License_Plate')
		_data_[0].State_province = request.form.get('State_province')
		_data_[0].VIN = request.form.get('VIN')
		db.session.add(_data_[0])
		db.session.commit()
		flash('Record Updated.')

	try:
		if (len(_truck_to_edit_)) < 1:
			newdata = ""
		else:
			newdata = _data_[0]
	except Exception as e:
		newdata = ""
	try:
		form = TruckForm(request.form, obj=_data_[0])
		form.populate_obj(_data_[0])
	except Exception as e:
		form = TruckForm(request.form)
	newdata = _data_[0]
	return render_template('edittruck.html', data = newdata, form=form, role = 2)