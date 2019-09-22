from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms.validators import AnyOf
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, DateTime, CHAR, Time, Boolean, Float
from flask.ext.login import AnonymousUserMixin
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)
import sqlalchemy
try:
    from webapp1.extensions import bcrypt
except Exception as e:
    print(e)
try:
    from extensions import bcrypt
except Exception as e:
    print(e)

db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Locations_Specific_To_Driver(db.Model):
    __tablename__ = 'eld_locations'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    todays_date = db.Column(db.Integer())
    this_id = db.Column(db.Integer())


    def __repr__(self):
        return '{},{},{},{}'.format(self.user_id, self.longitude, self.latitude, self.todays_date)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyid = db.Integer()
    first_name = db.Column(db.String(100))
    ELD_Account_Type = db.Integer()
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(1000))
    username = db.Column(db.String(64))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return "<User(companyid='%s', first_name='%s',ELD_Account_Type='%s', last_name='%s',login='%s', email='%s',username='%s', first_name='%s')>" % (self.companyid, self.first_name,self.ELD_Account_Type, self.last_name,self.login, self.email,self.username, self.first_name)
    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __repr__(self):

        return '{}'.format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

#
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])
        return user


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


    def __repr__(self):
        return '<Role {}>'.format(self.name)



class compass(db.Model):
    __tablename__ = 'compass'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    direction = db.Column(CHAR(50))
    direction = db.Column(CHAR(3))
    def __repr__(self):
        return "<compass(direction='%s', direction='%s')>" % (self.direction, self.direction)


class codrivers(db.Model):
    __tablename__ = 'codrivers'
    uid = Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer)
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    ELD_Username = Column(String(20))
    First_Name = Column(String(20))
    Last_Name = Column(String(20))
    Drivers_License = Column(String(25))
    Drivers_License_State = Column(String(2))
    Current_Device = Column(Integer)
    Current_Status = Column(Integer)
    exempt_driver = Column(CHAR(1))

    def __repr__(self):
        return "<codrivers(user_id='%s', First_Name='%s', Last_Name='%s', Drivers_License_State='%s'Drivers_License='%s', device_id='%s', Current_Status='%s')>" % (self.user_id, self.First_Name, self.Last_Name, self.Drivers_License_State, self.Drivers_License, self.device_id, self.Current_Status)


class drivers(db.Model):
    __tablename__ = 'drivers'
    uid = Column(db.Integer, primary_key=True, autoincrement=True)
    companyid = db.Integer()

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    #device_id = db.Column(db.Integer, db.ForeignKey('device.uid'))
    ELD_Username = Column(String(20))
    First_Name = Column(String(20))
    Last_Name = Column(String(20))
    Drivers_License = Column(String(25))
    Drivers_License_State = Column(String(2))
    Current_Device = Column(Integer)
    Current_Status = Column(Integer)
    exempt_driver = Column(CHAR(1))

    def __repr__(self):
        return "<drivers(user_id='%s', First_Name='%s', Last_Name='%s', Drivers_License_State='%s'Drivers_License='%s', device_id='%s', Current_Status='%s')>" % (self.user_id, self.First_Name, self.Last_Name, self.Drivers_License_State, self.Drivers_License, self.device_id, self.Current_Status)
        #return "{},{},{},{},{},{},{}".format(self.user_id, self.First_Name, self.Last_Name, self.Drivers_License_State, self.Drivers_License, self.device_id, self.Current_Status)

    # def __init__(self, company_id, user_id, firstname, lastname, driverslicense, driverslicensestate, currentstatus):
    #     self.company_id = company_id
    #     self.user_id = user_id
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.driverslicense = driverslicense
    #     self.driverslicensestate = driverslicensestate
    #     self.currentstatus = currentstatus


class Trailers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    companyid = db.Integer()
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer)
    todays_log = Column(Integer)
    Unit = db.Column(db.String(255))
    License_Plate = db.Column(db.String(20))
    State_Province = db.Column(db.String(20))

    def __repr__(self):
        return "<Trailers(company_id='%s', Unit='%s', License_Plate='%s', State_Province='%s')>" % (self.company_id, self.Unit, self.License_Plate, self.State_Province)

class company(db.Model):
    __tablename__ = "company"
    uid = Column(Integer, primary_key = True)
    companyname = Column(CHAR(100))
    address = Column(CHAR(100))
    city = Column(CHAR(100))
    postalcode = Column(CHAR(6))
    phonenumber = Column(CHAR(20))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # drivers_id = db.Column(db.Integer, db.ForeignKey('drivers.uid'))
    # device_id = db.Column(db.Integer, db.ForeignKey('device.uid'))
    #truck_id = db.Column(db.Integer, db.ForeignKey('truck.uid'))
    user_id = db.Column(db.Integer)
    drivers_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    truck_id = db.Column(db.Integer)


    def __repr__(self):
        return "<company(companyname='%s', address='%s', city='%s', postalcode='%s', phonenumber='%s')>" % (self.companyname, self.address, self.city, self.postalcode, self.phonenumber)




class RPM(db.Model):
    __tablename__ = "elog"
    uid = Column(Integer, primary_key = True, autoincrement = True)
    # EVENTSQUENCEID = Column(Integer)
    # EVENTTYPE = Column(Integer)
    # EVENTCODE = Column(Integer)
    # VEHICLEMILES = Column(Integer)
    # ENGINEHOURS = Column(Integer)
    # DISTANCESINCELASTVALIDCOORDINATES = Column(Integer)
    company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    driver_id = db.Column(db.Integer())
    device_id = db.Column(db.Integer(), db.ForeignKey('device.uid'))
    rpm = Column(Integer)
    status = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    datetimestamp = Column(Time(100))
    daterecorded = Column(DateTime)
    def __repr__(self):
        return '{}, {}'.format(self.rpm, self.driver_id, self.user_id, self.status)


class Event_Type(db.Model):
    __tablename__ = "event_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Event_Type = Column(CHAR(100))
    Event_Type_Code = Column(Integer)
    def __repr__(self):
        return "<Event_Type(Event_Type='%s', Event_Type_Code='%s')>" % (self.Event_Type, self.Event_Type_Code)


class Events(db.Model):
    __tablename__ = "events"
    id = Column(Integer, primary_key = True, autoincrement = True)
    #Type 1
    #companyid = db.Integer()
    Event_Sequence_ID_Number = Column(Integer)
    Event_Record_Status = Column(Integer)
    Event_Record_Origin = Column(Integer)
    Event_Type = Column(Integer)
    Event_Code = Column(Integer)
    Event_Date = Column(DateTime)
    Event_Time = Column(DateTime)
    Accumulated_Engine_Miles = Column(Integer)
    Elapsed_Engine_Hours = Column(Integer)
    Event_Latitude = Column(Float)
    Event_Longitude = Column(Float)
    Distance_Since_Last_Valid_Coordinates = Column(Integer)
    Malfunction_Indicator_Status = Column(Integer)
    Data_Diagnostic_Event_Indicator_Status = Column(Integer)
    Event_Comment = Column(CHAR)
    Drivers_Location_Description = Column(CHAR)
    Event_Data_Check_Value = Column(Integer)
    Odometer = Column(Integer)
    user_id = Column(Integer)
    device_id = Column(Integer)
    todays_log = Column(Integer)

    def __repr__(self):
        return "<Event_Type(Event_Sequence_ID_Number='%s', Event_Record_Status='%s', Event_Record_Origin='%s', Event_Type='%s', Event_Code='%s', Event_Date='%s', Event_Time='%s', Accumulated_Engine_Miles='%s', Elapsed_Engine_Hours='%s', Event_Latitude='%s', Event_Longitude='%s', Distance_Since_Last_Valid_Coordinates='%s', Event_Comment='%s', Event_Data_Check_Value='%s', Odometer='%s')>" % (self.Event_Sequence_ID_Number, self.Event_Record_Status, self.Event_Record_Origin, self.Event_Type, self.Event_Code, self.Event_Date, self.Event_Time, self.Accumulated_Engine_Miles, self.Elapsed_Engine_Hours, self.Event_Latitude, self.Event_Longitude, self.Distance_Since_Last_Valid_Coordinates, self.Event_Comment, self.Event_Data_Check_Value, self.Odometer)


class Events_Codes(db.Model):
    __tablename__ = "events_codes"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(CHAR(100))
    def __repr__(self):
        return "<Event_Codes(name='%s')>" % (self.name)


class Locations(db.Model):
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(CHAR(100))
    abbreviation = Column(CHAR(10))
    country = Column(CHAR(30))
    def __repr__(self):
        return "<Locations(name='%s',abbreviation='%s',country='%s')>" % (self.name, self.abbreviation, self.country)


class Events_Log(db.Model):
    __tablename__ = "events_log"
    Event_Sequence_ID_Number = Column(Integer, primary_key = True, autoincrement = True)
    Event_Date = Column(DateTime)
    Event_Time = Column(DateTime)
    Log_Date = Column(CHAR(20))
    Location = Column(CHAR(100))
    Odometer = Column(Integer)
    Engine_Hours = Column(Integer)
    Event_Type = Column(Integer)
    Origin = Column(Integer)
    Event_Code = Column(Integer)
    Locations_id = db.Column(db.Integer(), db.ForeignKey(Locations.id))
    #Locations = db.relationship(Locations, backref='events_log')
    Events_Codes_id = db.Column(db.Integer(), db.ForeignKey(Events_Codes.id))
    #Events_Codes = db.relationship(Events_Codes, backref='events_log')
    #Events = Column(CHAR(100))

    def __repr__(self):
        return '{},{},{},{},{},{},{},{}'.format(self.Event_Date,self.Event_Time,self.Location,self.Odometer, self.Engine_Hours, self.Event_Type, self.Origin, self.Event_Code)




class Documents(db.Model):
    __tablename__ = "documents"
    id = Column(Integer, primary_key = True, autoincrement = True)
    documentnumber = Column(Integer)

    def __repr__(self):
        return "<Documents(documentnumber='%s')>" % (self.documentnumber)


class Device(db.Model):
    __tablename__ = "device"
    uid = Column(Integer, primary_key = True)
    companyid = db.Integer()
    #companyid = db.relationship('company', backref='devices',                                lazy='dynamic')
    #driver_id = Column(Integer, sqlalchemy.ForeignKey('drivers.uid'))
    driver_id = Column(Integer)
    #driver_id = Column(Integer))
    #driverid = db.relationship('drivers', backref='Device')
    devicename = Column(String)
    status = Column(Integer)
    Device_Number = Column(String)
    def __repr__(self):
        return "<Device(devicename='%s',status='%s',Device_Number='%s')>" % (self.devicename,self.status,self.Device_Number)

        
class truck(db.Model):
    __tablename__ = 'truck'
    uid = Column(Integer, primary_key = True, autoincrement=True)
    companyid = Column(Integer)
    unit = Column(String(20))
    License_Plate = Column(String(20))
    State_province = Column(String(20))
    VIN = Column(String(20))
    user_id = Column(Integer)
    def __repr__(self):
        return "<truck(uid='%s', unit='%s',License_Plate='%s',State_provice='%s',VIN='%s', user_id ='%s')>" % (self.uid, self.unit,self.License_Plate,self.State_province,self.VIN, self.user_id)
        #return '{},{},{}'.format(self.unit, self.License_Plate,self.State_province)




class Truck(db.Model):
    __tablename__ = 'Trucks'
    uid = Column(Integer, primary_key = True, autoincrement=True)
    companyid = db.Integer()
    unit = Column(String(20))
    License_Plate = Column(String(20))
    State_province = Column(String(20))
    VIN = Column(String(20))
    user_id = Column(Integer)
    def __repr__(self):
        return "<Truck(unit='%s',License_Plate='%s',State_provice='%s',VIN='%s')>" % (self.unit, self.License_Plate, self.State_province, self.VIN)



   
class DVIR(db.Model):
    __tablename__ = 'dvir'
    id = Column(Integer, primary_key = True, autoincrement=True)
    company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
    #truck_id = Column(Integer, sqlalchemy.ForeignKey('truck.uid'))
    #truck = db.relationship('truck', backref='dvir')
    Signature = Column(Boolean)
    General = Column(Boolean)
    DriverController = Column(Boolean)
    HeaterDefroster = Column(Boolean)
    Horn = Column(Boolean)
    Steering = Column(Boolean)
    DriverSeat = Column(Boolean)
    GlassandMirrors = Column(Boolean)
    Windshield = Column(Boolean)
    EmergencyEquipment = Column(Boolean)
    FuelSystem = Column(Boolean)
    AirBrakeSystem = Column(Boolean)
    Tires = Column(Boolean)
    Tires = Column(Boolean)
    Wheels = Column(Boolean)
    SuspensionSystem = Column(Boolean)
    CouplingDevices = Column(Boolean)
    Lamps= Column(Boolean)
    DangerousGoods = Column(Boolean)
    ExhaustSystem = Column(Boolean)
    Frameandcargo = Column(Boolean)
    cargosecurement = Column(Boolean)
    hydraulicbrakes = Column(Boolean)
    electricbraks = Column(Boolean)
    Majordefectsnotcodedabove = Column(Boolean)
    TimeofInspection = Column(Boolean)
    Dateofinspection = Column(Boolean)
    Odometer = Column(Boolean)
    LocationofInspection = Column(Boolean)
    TrailerLicensePlate = Column(Boolean)
    InspectorName = Column(Boolean)
    driver_id = Column(Integer, sqlalchemy.ForeignKey('drivers.uid'))
    Trailer = Column(Boolean)
    def __init__(self, DriverController,HeaterDefroster,Horn,Steering,DriverSeat,GlassandMirrors,Windshield,EmergencyEquipment,FuelSystem,AirBrakeSystem,Tires,Wheels,SuspensionSystem,CouplingDevices,Lamps,ExhaustSystem,Frameandcargo,cargosecurement,hydraulicbrakes, electricbraks,Majordefectsnotcodedabove,TimeofInspection,Dateofinspection,Odometer,LocationofInspection,TrailerLicensePlate,InspectorName,Trailer):
        # self.truck_id  =  truck_id 
        # self.truck  =  truck 
        # self.Signature  =  Signature 
        # self.General  =  General 
        self.DriverController  =  DriverController 
        self.HeaterDefroster  =  HeaterDefroster 
        self.Horn  =  Horn 
        self.Steering  =  Steering 
        self.DriverSeat  =  DriverSeat 
        self.GlassandMirrors  =  GlassandMirrors 
        self.Windshield  =  Windshield 
        self.EmergencyEquipment  =  EmergencyEquipment 
        self.FuelSystem  =  FuelSystem 
        self.AirBrakeSystem  =  AirBrakeSystem 
        self.Tires  =  Tires 
        self.Tires  =  Tires 
        self.Wheels  =  Wheels 
        self.SuspensionSystem  =  SuspensionSystem 
        self.CouplingDevices  =  CouplingDevices 
        self.Lamps =  Lamps
        self.ExhaustSystem  =  ExhaustSystem 
        self.Frameandcargo  =  Frameandcargo 
        self.cargosecurement  =  cargosecurement 
        self.hydraulicbrakes  =  hydraulicbrakes 
        self.electricbraks  =  electricbraks 
        self.Majordefectsnotcodedabove  =  Majordefectsnotcodedabove 
        self.TimeofInspection  =  TimeofInspection 
        self.Dateofinspection  =  Dateofinspection 
        self.Odometer  =  Odometer 
        self.LocationofInspection  =  LocationofInspection 
        self.TrailerLicensePlate  =  TrailerLicensePlate 
        self.InspectorName  =  InspectorName 
    def __repr__(self):
        return "<DVIR(unit='%s',License_Plate='%s',State_provice='%s',VIN='%s')>" % (self.unit, self.License_Plate, self.State_province, self.VIN)

class IFTA(db.Model):
    __tablename__ = 'IFTA'
    id = Column(Integer, primary_key = True)
    companyid = db.Integer()
    datetime = Column(Integer, primary_key = True)
    longitude = Column(Integer, primary_key = True)
    latitude = Column(Integer, primary_key = True)

