from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.models import DVIR, db
from webapp1.forms import DVIRForm
dvir_blueprint = Blueprint(
	'dvir',
	__name__,
	template_folder='../templates/dvir',
	url_prefix="/dvir"
	)



@dvir_blueprint.route('/')
@dvir_blueprint.route('/createdvir', methods=('GET','POST'))
def home():
	form = DVIRForm()

	try:
		DriverController = request.form.get('DriverController')
		HeaterDefroster = request.form.get('HeaterDefroster')
		Horn = request.form.get('Horn')                
		Steering = request.form.get('Steeringe')
		DriverSeat = request.form.get('DriverSeat')
		GlassandMirrors = request.form.get('GlassandMirrors')
		Windshield = request.form.get('Windshield')
		EmergencyEquipment= request.form.get('EmergencyEquipment')
		FuelSystem = request.form.get('FuelSystem')                        
		AirBrakeSystem = request.form.get('AirBrakeSystem')
		Tires = request.form.get('Tires')
		Wheels = request.form.get('Wheels')
		SuspensionSystem = request.form.get('SuspensionSystem')
		CouplingDevices = request.form.get('CouplingDevices')
		Lamps = request.form.get('Lamps')                       
		ExhaustSystem = request.form.get('ExhaustSystem')
		Frameandcargo = request.form.get('Frameandcargo')
		cargosecurement = request.form.get('cargosecurement')
		hydraulicbrakes = request.form.get('hydraulicbrakes')
		electricbraks = request.form.get('electricbraks')
		Majordefectsnotcodedabove = request.form.get('Majordefectsnotcodedabove')
		Lamps = request.form.get('Lamps')                       
		TimeofInspection = request.form.get('TimeofInspection')
		Dateofinspection = request.form.get('Dateofinspection')
		Odometer = request.form.get('Odometer')   
		LocationofInspection = request.form.get('LocationofInspection')                       
		TrailerLicensePlate = request.form.get('TrailerLicensePlate')
		InspectorName = request.form.get('InspectorName')
		Trailer = request.form.get('Trailer')   

		dvir = DVIR(DriverController,HeaterDefroster,Horn, Steering,DriverSeat,GlassandMirrors,Windshield,EmergencyEquipment,FuelSystem,AirBrakeSystem,Tires,Wheels,SuspensionSystem,CouplingDevices,Lamps,ExhaustSystem,Frameandcargo,cargosecurement,hydraulicbrakes, electricbraks,Majordefectsnotcodedabove,TimeofInspection,Dateofinspection,Odometer,LocationofInspection,TrailerLicensePlate,InspectorName,Trailer)
		db.session.add(dvir)
		db.session.commit()
	except Exception as e:
		print(e)
		db.session.rollback()
	if not current_user.is_authenticated:
		return redirect(url_for('admin.login_view'))
	return render_template('createdvir.html', form = form)


@dvir_blueprint.route('/update-dvir', methods=('GET','POST'))
def updatedvir():
    form = DVIRForm()
    return render_template('createdvir.html', form=form)


@dvir_blueprint.route('/show-dvir', methods=('GET','POST'))
def showdvir():
    form = DVIRForm()
    return render_template('createdvir.html', form=form)
