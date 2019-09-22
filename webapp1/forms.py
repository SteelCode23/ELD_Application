from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import TextField
from wtforms import validators
from wtforms import SelectField
from wtforms import TextAreaField
import wtforms
#from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField
from wtforms.fields import BooleanField, DateField,IntegerField
class RegistrationForm(Form):
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(),
                              validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(),
                               validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [validators.DataRequired()])


class LoginForm(Form):
    loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    loginpassword = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
    submit = SubmitField('submit', [validators.DataRequired()])


class CreateTableForm(Form):
    tablenumber = TextField('tablenumber', validators=[validators.DataRequired()])
    submit = SubmitField('createtablesubmit', validators=[validators.DataRequired()])


class QueryForm(Form):
    Query= TextField('query', validators=[validators.DataRequired()])
    Store = SelectField('Campaign', choices = [('tepp','Teppermains Main'), ('ba','Bargain Annex')],validators=[validators.DataRequired()])
    Category = SelectField('Campaign', choices = [('tepp','Teppermains Main'), ('ba','Bargain Annex')],validators=[validators.DataRequired()])
    submit = SubmitField('Query Documents', validators=[validators.DataRequired()])



class ElogForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    ondutydriving = SubmitField('On Duty', validators=[validators.DataRequired()])
    ondutynotdriving = SubmitField('On Duty Not Driving', validators=[validators.DataRequired()])
    ondutysleeping = SubmitField('On Duty Sleeping', validators=[validators.DataRequired()])
    offduty = SubmitField('Off Duty', validators=[validators.DataRequired()])
    Authorized = SubmitField('Authorized Personal Use of CMV', validators=[validators.DataRequired()])
    YardMoves = SubmitField('Yard Moves', validators=[validators.DataRequired()])
    Cleared = SubmitField('PC, YM, and WT Cleared', validators=[validators.DataRequired()])
    loaddata = SubmitField('Load Data', validators=[validators.DataRequired()])
    rpm = TextField('rpm', validators=[validators.DataRequired()])
    certify = SubmitField('Certify', validators=[validators.DataRequired()]) 
    rate = TextField('rpm')
       
    #location = TextField('location', validations.DataRequired())


class TruckForm(Form):

    unit = TextField('Unit Number', validators=[validators.DataRequired()])
    License_Plate = TextField('License Plate', validators=[validators.DataRequired()])
    State_province = SelectField('License Plate State or Province of Registration', choices = [('ON','ON'), ('QC','QC'), ('MI','MI')],validators=[validators.DataRequired()])
    VIN = TextField('VIN Number', validators=[validators.DataRequired()])
    # submit = SubmitField('Save', validators=[validators.DataRequired()])

class EmailServicesForm(Form):
    submit = SubmitField('Send Data', validators=[validators.DataRequired()])
    email = TextField('Email Address', validators=[validators.DataRequired()])


class BluetoothServicesForm(Form):
    submit = SubmitField('Send Data', validators=[validators.DataRequired()])
    email = TextField('Email Address', validators=[validators.DataRequired()])


class USBServicesForm(Form):
    #This should bring up perhaps windows explorer....or  at least generate the location to select the file from.
    submit = SubmitField('Send Data', validators=[validators.DataRequired()])
    email = TextField('Email Address', validators=[validators.DataRequired()])



class CertifyForm(Form):
    #This should bring up perhaps windows explorer....or  at least generate the location to select the file from.
    agree = SubmitField('Agree', validators=[validators.DataRequired()])
    disagree = SubmitField('Not Ready', validators=[validators.DataRequired()])    


class WIFIservicesForm(Form):
    #This should bring up perhaps windows explorer....or  at least generate the location to select the file from.
    submit = SubmitField('Send Data', validators=[validators.DataRequired()])
    email = TextField('Email Address', validators=[validators.DataRequired()])




class DriverForm(Form):

    First_Name = TextField('First Name', validators=[validators.DataRequired()])
    Last_Name = TextField('Last Name', [validators.Required("Please enter the driver's last name")])
    Drivers_License = TextField('Drivers License', validators=[validators.DataRequired()])
    Drivers_License_State = SelectField('Drivers License State or Province of Registration', choices = [('ON','ON'), ('QC','QC'), ('MI','MI')],validators=[validators.DataRequired()])
    Drivers_Rotation = SelectField('Rotation', choices = [('72-Hour','72-Hour'), ('40-Hour','40-Hour')],validators=[validators.DataRequired()])
    #submit = SubmitField('Submit', validators=[validators.DataRequired()])

class DevicesForm(Form):
    submit = SubmitField('Add Device', validators=[validators.DataRequired()])
    Device_Number = TextField('Device Number', validators=[validators.DataRequired()])
    devicename = TextField('Device Name', validators=[validators.DataRequired()])


class DVIRForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    firstname = TextField('First Name', validators=[validators.DataRequired()])
    lastname = TextField('Last Name', validators=[validators.DataRequired()])
    driverslicense = TextField('Drivers License', validators=[validators.DataRequired()])
    Signature = BooleanField('Signature')
    General = BooleanField('General')
    DriverController = BooleanField('DriverController')
    HeaterDefroster = BooleanField('HeaterDefroster ')
    Horn = BooleanField('Horn')
    Steering = BooleanField('Steering')
    DriverSeat = BooleanField('DriverSeat')
    GlassandMirrors = BooleanField('Glass and Mirrors')
    Windshield = BooleanField('Windshield')
    EmergencyEquipment = BooleanField('EmergencyEquipment')
    FuelSystem = BooleanField('FuelSystem')
    AirBrakeSystem = BooleanField('AirBrakeSystem')
    Tires = BooleanField('Tires')
    Wheels = BooleanField('Wheels')
    SuspensionSystem = BooleanField('SuspensionSystem')
    CouplingDevices = BooleanField('CouplingDevices')
    Lamps= BooleanField('Lamps')
    ExhaustSystem = BooleanField('ExhaustSystem')
    ExhaustSystem = BooleanField('ExhaustSystem')
    Frameandcargo = BooleanField('Frameandcargo')
    cargosecurement = BooleanField('cargosecurement')
    hydraulicbrakes = BooleanField('hydraulicbrakes')
    electricbraks = BooleanField('electricbraks')
    Majordefectsnotcodedabove = BooleanField('Majordefectsnotcodedabove')
    #Will need to be change to some sort of datetime stamp
    TimeofInspection = DateField('Time of Inspection')
    Dateofinspection = DateField('Date of Inspection')
    Odometer = IntegerField('Odometer')
    LocationofInspection = TextField('Location of Inspection')
    TrailerLicensePlate = TextField('Trailer License Plate')
    InspectorName = TextField('Inspector Name')
    Trailer = TextField('Trailer')

class ContactForm(Form):
    name = TextField("Name",  [validators.Required("Please enter your name.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")