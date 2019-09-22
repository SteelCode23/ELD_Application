from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.extensions import poster_permission, admin_permission
from webapp1.forms import DriverForm, ElogForm, EmailServicesForm, BluetoothServicesForm, USBServicesForm, \
    WIFIservicesForm, CertifyForm
from webapp1.models import drivers, db, RPM, User, Events
import datetime
from sqlalchemy import update
import random

logs_blueprint = Blueprint(
    'logs',
    __name__,
    template_folder='../templates/logs',
    url_prefix="/logs"
)


##OBD simulator
#Simulates J1939 data feeding this truck:
#Send request for RPM
#Receives data triggers all the events...
#Updates Events Table
#newevents = Events()
#db.session.add(Events)
#try:
#    db.session.commit()
#except Exception as e:
#    db.session.rollback



@logs_blueprint.route('/certify', methods=['GET', 'POST'])
def certifylogs():
    certify = CertifyForm(request.form)
    return render_template('certifylogs.html', role = 1, certify = certify)


@logs_blueprint.route('/certifylogsaccept', methods=['GET', 'POST'])
def certifylogscomplete():
    certify = CertifyForm(request.form)
    data =str(datetime.datetime.today().day) + "" +  str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
    thisdate_ = int(data)
    previousmax = db.engine.execute('select max("Event_Code") from events where events.todays_log = %s and user_id = %s',[int(data), current_user.get_id()])

    try:
        for i in previousmax:
            data = i
            data = data[0]
        if(int(data) > 8):
            eventrecord = 9
        else:
            eventrecord = data + 1
    except Exception as e:
        eventrecord = 1
    event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 4, Event_Code = int(eventrecord), Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id(), todays_log = thisdate_)
    db.session.add(event)
    db.session.commit()   
    #form = DriverForm(request.form)
    return render_template('certifylogs.html', role = 1, certify = certify)


@logs_blueprint.route('/gasoline', methods=['GET', 'POST'])
def gasoline():
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
    except Exception as e:
        print(e)
        db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('gasoline.html', form=form, elog=elog, role = 2)


@logs_blueprint.route('/roadside', methods=['GET', 'POST'])
def logs():
    # This is going to return a list of dictionaries that will generate the table in the logs.html template
    # It will start with some sort of query that will iterate over the results and encode them into the list of dictionaries.
    # For example
    counter = 0
    list_ = []
    for i in range(0, 96):
        list__ = []
        counter = counter + .25
        list__.append(counter)
        list__.append(random.randint(1, 4))
        list_.append(list__)

    date = request.form.get('datefrom')

    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        date = request.form.get('datefrom')
    except Exception as e:
        date = "2017-11-27"
        # date = "2017-03-03"
    # Injecting to test this new filtering events method
    try:
        data = date.split('/')
    except Exception as e:
        date = str(datetime.datetime.today().month) + "/" + str(datetime.datetime.today().day) + "/" + str(
            datetime.datetime.today().year)
        data = date.split('/')
        date = str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day) + "-" + str(
            datetime.datetime.today().year)

    dateforfiltering = str(date).split("-")
    dateforfiltering = str(dateforfiltering[2]) + "" + str(dateforfiltering[1]) + "" + str(dateforfiltering[0])
    date_to_redirect_to_edit = str(dateforfiltering[2]) + "-" + str(dateforfiltering[1]) + "-" + str(
        dateforfiltering[0])
    thisdata_ = Events.query.filter_by(todays_log=int(dateforfiltering)).all()
    newlist_ = []
    for i in thisdata_:
        # (str(i).split(",")
        newlist_.append(str(i).split(","))

    # Google Charts working code for logs
    stateinitial = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 8]
    reportinglist = []
    for i in range(0, len(newlist_)):
        # if(int(rows[1][0]) > 499):
        newdata = []
        try:
            newdata.append(int(i))
            newdata.append(int(newlist_[i][6]))

            reportinglist.append(newdata)
        except Exception as e:
            print(e)
    current_status = 'driving'
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))

    return render_template('logs.html', form=form, elog=elog, role=1, current_status=current_status,
                           events_log=newlist_, logdata=reportinglist, thiddate_=dateforfiltering,
                           date_to_redirect_to_edit=date_to_redirect_to_edit)




@logs_blueprint.route('/showlogs', methods=['GET', 'POST'])
def logs1():
    #This is going to return a list of dictionaries that will generate the table in the logs.html template
    #It will start with some sort of query that will iterate over the results and encode them into the list of dictionaries.
    # For example
    _driver_ = request.args.get("driverid")
    counter = 0
    list_ = []
    for i in range(0,96):
        list__ = []
        counter = counter + .25
        list__.append(counter)
        list__.append(random.randint(1,4))
        list_.append(list__)
    
    date = request.form.get('datefrom')
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        date = request.form.get('datefrom')
        date = 2932018
    except Exception as e:
        date = "2017-11-27"
        # date = "2017-03-03"
    #Injecting to test this new filtering events method
    try:
        data = date.split('/')
    except Exception as e:
        date = str(datetime.datetime.today().month) + "/" + str(datetime.datetime.today().day) + "/" + str(datetime.datetime.today().year)
        data = date.split('/')
        date = str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day) + "-" + str(datetime.datetime.today().year)


    dateforfiltering = str(date).split("-")
    dateforfiltering = str(dateforfiltering[2]) + "" + str(dateforfiltering[1]) + "" + str(dateforfiltering[0])
    date_to_redirect_to_edit = str(dateforfiltering[2]) + "-" + str(dateforfiltering[1]) + "-" + str(dateforfiltering[0])
    thisdata_ = Events.query.filter_by(todays_log=int('3032018')).all()
    newlist_ = []
    for i in thisdata_:
        #(str(i).split(",")
        newlist_.append(str(i).split(","))


    #Google Charts working code for logs
    stateinitial = [0,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,8]
    reportinglist = []
    for i in range(0,len(newlist_)):
        # if(int(rows[1][0]) > 499):
        newdata = []
        try:
            newdata.append(int(i))
            newdata.append(int(newlist_[i][6]))

            reportinglist.append(newdata)
        except Exception as e:
            print(e)
    current_status = 'driving'
    # if not current_user.is_authenticated:
    #     return redirect(url_for('admin.login_view'))
    _date_ = request.args.get("log_date")
    #if len(str(_date_)) < 1:
    _data_ = '2932018'
    event_log = Events.query.filter_by(todays_log=int('2932018')).all()
    return render_template('logs.html', form=form, elog=elog,  role = 2, current_status = current_status, events_log = event_log, logdata = reportinglist, thiddate_ = dateforfiltering, date_to_redirect_to_edit = date_to_redirect_to_edit)


@logs_blueprint.route('/showlogs_driver', methods=['GET', 'POST'])
def logs_driver():
    date = request.form.get('datefrom')
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        date = request.form.get('datefrom')
    except Exception as e:
        date = "2017-03-03"
        # date = "2017-03-03"
    print(date)
    todayslog___ = date.split("-")
    todayslog___ = str(todayslog___[2]) + "" + str(todayslog___[1]) + "" +  str(todayslog___[0])
    # date = "2017-03-03"
    data = Events.query.filter_by(todays_log=todayslog___).all()

    # data = RPM.query.filter_by(user_id=current_user.get_id(), daterecorded=date).all()
    # print(data)
    stateinitial = []
    for i in data:
        stateinitial.append(int(i.rpm))

    timestate = []
    state = []
    counter = 1
    newlist = []

    for i in range(0, len(stateinitial)):
        # if(int(rows[1][0]) > 499):
        newval = random.randint(450, 600)

        if (stateinitial[i] > 499):
            state.append(1)
            timestate.append(counter)
        else:
            state.append(0)
            timestate.append(counter)
        counter += 1

    for i in range(1, len(state)):
        try:
            if (state[i] != state[i + 1]):
                newlist.append(i + 1)
        except Exception as e:
            print(e)
    counter = 0
    for i in newlist:
        if (state[i + counter] == 1):
            state.insert(i + counter, 1)
            timestate.insert(i + counter, i)
        else:
            state.insert(i + counter, 0)
            timestate.insert(i + counter, i)
        counter += 1
    data = state
    xdata = timestate

    # if not current_user.is_authenticated:
    #     return redirect(url_for('admin.login_view'))
    return render_template('logs.html', form=form, elog=elog, xdata=xdata, data=data, datedata=date, role = 2)


# AJAX
@logs_blueprint.route('/DRIVING', methods=['GET'])
def driving():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("Driving")
    if(datetime.datetime.today().day) < 10:
        today_ = "0" + str(datetime.datetime.today().day)
    else:
        today_ = str(datetime.datetime.today().day)
    todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
    db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [1, current_user.get_id()])
    db.session.commit()
    event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 3, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), todays_log = todaysdate_)
    db.session.add(event)
    db.session.commit()    
    #db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [1, 1])
    return jsonify(result="Driving")

    # id = Column(Integer, primary_key = True, autoincrement = True)
    # #Type 1
    # Event_Sequence_ID_Number = Column(Integer)
    # # Description : This data element refers to the serial identifier assigned to each required
    # ELD event as described in section 4.5.1 of this appendix.
    # Purpose : Provides ability to keep a continuous record, on a given ELD, across all
    # users of that ELD.
    # Source : ELD internal calculations.
    # Used in : ELD event records; ELD outputs.
    # Data Type : ELD maintained; incremented by 1 for each new record on the ELD;
    # continuous for each new event the ELD records regardless of owner of the records.
    # Data Range : 0 to FFFF; initial factory value must be 0; after FFFF hexadecimal
    # (decimal 65535), the next Event Sequence ID number must be 0. 
    # 148
    # Data Length : 1-4 characters.
    # Data Format : <Event Sequence ID Number > as in <C> to <CCCC>.
    # Disposition : Mandatory.
    # Examples : [1], [1F2C], [2D3], [BB], [FFFE]. 
    # Event_Sequence_ID_Number = Column(Integer)
    # Event_Record_Status = Column(Integer)
    # Event_Record_Origin = Column(Integer)
    # Event_Type = Column(Integer)
    # Event_Code = Column(Integer)    

    # 7.23 Event Record Status
    # Description : An attribute for the event record indicating whether an event is active or
    # inactive and further, if inactive, whether it is due to a change or lack of confirmation by
    # the driver or due to a driver’s rejection of change request.
    # Purpose : Provides ability to keep track of edits and entries performed over
    # ELD records while retaining original records.
    # Source : ELD internal calculations.
    # Used in : ELD event records; ELD outputs.
    # Data Type : ELD recorded and maintained event attribute in accordance with the
    # procedures outlined in sections 4.4.4.2.2, 4.4.4.2.3, 4.4.4.2.4, 4.4.4.2.5, and 4.4.4.2.6 of
    # this appendix.
    # Data Range : 1, 2, 3 or 4 as described on Table 8 of this appendix. 
    # 147
    # Data Length : 1 character.
    # Data Format : <Event Record Status> as in <C>.
    # Disposition : Mandatory.
    # Examples : [1], [2], [3], [4] 


    # Event_Record_Origin = Column(Integer)
    # Description : An attribute for the event record indicating whether it is automatically
    # recorded, or edited, entered or accepted by the driver, requested by another authenticated
    # user, or assumed from unidentified driver profile.
    # Purpose : Provides ability to track origin of the records.
    # Source : ELD internal calculations.
    # Used in : ELD event records; ELD outputs.
    # Data Type : ELD recorded and maintained event attribute in accordance with the
    # procedures outlined in sections 4.4.4.2.2, 4.4.4.2.3, 4.4.4.2.4, 4.4.4.2.5, and 4.4.4.2.6 of
    # this appendix.
    # Data Range : 1, 2, 3 or 4 as described on Table 7 of this appendix.
    # Data Length : 1 character.
    # Data Format : <Event Record Origin> as in <C>.
    # Disposition : Mandatory. 
    # 146
    # Examples : [1], [2], [3], [4]. 

    # Event_Type = Column(Integer)
    # Description : An attribute specifying the type of the event record.
    # Purpose : Provides ability to code the type of the recorded event in electronic
    # format.
    # Source : ELD internal calculations.
    # Used in : ELD event records; ELD outputs.
    # Data Type : ELD recorded and maintained event attribute in accordance with the type
    # of event being recorded.
    # Data Range : 1-7 as described on Table 9 of this appendix.
    # Data Length : 1 character.
    # Data Format : <Event Type> as in <C>.
    # Disposition : Mandatory.
    # Examples : [1], [5], [4], [7].
    # Table 9
    # “Event Type” Parameter Coding
    # Event Type Event Type Code
    # A change in driver’s duty-status 1
    # An intermediate log 2 
    # 149
    # A change in driver’s indication of authorized personal use of
    # CMV or yard moves
    # 3
    # A driver’s certification/re-certification of records 4
    # A driver’s login/logout activity 5
    # CMV’s engine power up / shut down activity 6
    # A malfunction or data diagnostic detection occurrence 7 


    # Event_Code = Column(Integer)
    # Description : A dependent attribute on “Event Type” parameter that further specifies
    # the nature of the change indicated in “Event Type”; t`his parameter indicates the new
    # status after the change.
    # Purpose : Provides ability to code the specific nature of the change electronically.
    # Source : ELD internal calculations.
    # Used in : ELD event records; ELD outputs.
    # Data Type : ELD recorded and maintained event attribute in accordance with the type
    # of event and nature of the new status being recorded.
    # Data Range : Dependent on the “Event Type” as indicated on Table 6 of this appendix.
    # Data Length : 1 character.
    # Data Format : <Event Type> as in <C>.
    # Disposition : Mandatory.
    # Examples : [0], [1], [4], [9]. 


    # Event_Date = Column(Date)
    # Event_Time = Column(Time)
    # Accumulated_Engine_Miles = Column(Integer)
    # Elapsed_Engine_Hours = Column(Integer)
    # Description : This data element refers to the time the CMV’s engine is powered in
    # decimal hours with 0.1 hr (6-minute) resolution; this parameter is a placeholder for
    # <{Total} Engine Hours>, which refers to the aggregated time of a vehicle’s engine’s
    # operation since its inception, and used in recording “engine power on” and “engine shut
    # down” events, and also for <{Elapsed} Engine Hours>, which refers to the elapsed time
    # in the engine’s operation in the given ignition power on cycle, and used in the recording
    # of all other events.
    # Purpose : Provides ability to identify gaps in the operation of a CMV, when the
    # vehicle’s engine may be powered but the ELD may not; provides ability to cross check
    # integrity of recorded data elements in events and prevent gaps in the recording of ELD.
    # Source : ELD measurement or sensing.
    # Used in : ELD events; ELD outputs.
    # Data Type : Acquired from the engine ECM or a comparable other source as allowed
    # in section 4.3.1.4.
    # Data Range : For <{Total} Engine Hours>, range is between 0.0 and 99,999.9; for
    # <{Elapsed} Engine Hours>, range is between 0.0 and 99.9.
    # Data Length : 3-7 characters.
    # Data Format : <Vehicle Miles> as in <C.C> to <CCCCC.C>.
    # Disposition : Mandatory.
    # Examples : [0.0], [9.9], [346.1], [2891.4]. 


    # Event_Latitude = Column(Float)
    # Event_Longitude = Column(Float)
    # Distance_Since_Last_Valid_Coordinates = Column(Integer)
    # Malfunction_Indicator_Status = Column(Integer)
    # # Description : A code that further specifies the underlying malfunction or data
    # # diagnostic event.
    # # Purpose : Enables coding the type of malfunction and data diagnostic event to
    # # cover the standardized set in Table 4 of this appendix.
    # # Source : ELD internal monitoring.
    # # Used in : ELD events; ELD outputs.
    # # Data Type : Recorded by ELD when malfunctions and data diagnostic events are set
    # # or reset. 
    # # 157
    # # Data Range : As specified in Table 4 of this appendix.
    # # Data Length : 1 character.
    # # Data Format : <C>.
    # # Disposition _ : Mandatory.
    # # Examples : [1], [5], [P], [L]. 
    
    # Data_Diagnostic_Event_Indicator_Status = Column(Integer)
    # Event_Comment = Column(Char)
    # Drivers_Location_Description = Column(Char)
    # Event_Data_Check_Value = Column(Integer)
    #Type 2(b) 


@logs_blueprint.route('/ONDUTY', methods=['GET'])
def onduty():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("on duty")
    try:
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [2, current_user.get_id()])
        db.session.commit()
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 4, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(),user_id = current_user.get_id() , todays_log = todaysdate_)
        db.session.add(event)
        db.session.commit()


    except Exception as e:
        print(e)
    return jsonify(result="On Duty")


@logs_blueprint.route('/SLEEPING', methods=['GET'])
def sleeping():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [3, current_user.get_id()])
        db.session.commit()
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 2, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id(), device_id = driver_id, todays_log = todaysdate_)
        db.session.add(event)
        db.session.commit()        

    except Exception as e:
        print(e)
    print("Sleep")
    return jsonify(result="Sleeping")


@logs_blueprint.route('/OFFDUTY', methods=['GET'])
def offduty():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [4, current_user.get_id()])
        db.session.commit()
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 1, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id(), device_id = driver_id, todays_log = todaysdate_)
        db.session.add(event)
        db.session.commit()    
    except Exception as e:
        print(e)
    print("off duty")
    return jsonify(result="Off Duty")


@logs_blueprint.route('/authorized', methods=['GET'])
def authorized():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [4, current_user.get_id()])
        db.session.commit()
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 3, Event_Code = 1, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id(), device_id = driver_id, todays_log = todaysdate_)
        db.session.add(event)
        db.session.commit()    
    except Exception as e:
        print(e)
    return jsonify(result="Authorized Personal Use of CMV")


@logs_blueprint.route('/yard', methods=['GET'])
def yard():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 3, Event_Code = 2, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id())
        db.session.add(event)
        db.session.commit()    
    except Exception as e:
        print(e)
    print("off duty")
    return jsonify(result="Yard Moves")


@logs_blueprint.route('/cleared', methods=['GET'])
def cleared():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        driverid_1 = db.engine.execute('select uid from drivers where user_id = %s', [current_user.get_id()])
        for i in driverid_1 :
            driver_id = i[0]
        if (datetime.datetime.today().day) < 10:
            today_ = "0" + str(datetime.datetime.today().day)
        else:
            today_ = str(datetime.datetime.today().day)
        todaysdate_ = str(today_) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
        event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 3, Event_Code = 0, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now(), user_id = current_user.get_id(), todays_log = todaysdate_)
        db.session.add(event)
        db.session.commit()    
    except Exception as e:
        print(e)
    print("off duty")
    return jsonify(result="Indication for PC, YM, and WT Cleared")