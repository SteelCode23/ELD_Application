from __future__ import print_function
import requests
from datetime import datetime
import datetime
import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import pdb
import bs4
from email import encoders
import json
import base64
import openpyxl
import pandas as pd
import shutil
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.extensions import poster_permission, admin_permission
from webapp1.forms import DriverForm, ElogForm, EmailServicesForm, BluetoothServicesForm, USBServicesForm, WIFIservicesForm
from webapp1.models import RPM, User
from flask_mail import Message, Mail


webservices_blueprint = Blueprint(
    'webservices',
    __name__,
    template_folder='../templates/webservices',
    url_prefix="/webservices"
    )


#Am debating sending this over web services or directly...what does directly mean?? Also give ability to email
@webservices_blueprint.route('/senddata', methods = ['GET', 'POST'])
def SendData():
    elog = ElogForm(request.form)
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddata.html',elog=elog)


@webservices_blueprint.route('/senddataemail', methods = ['GET', 'POST'])
def SendDataEmail():
    mail = Mail()
    # form = ContactForm()
    request.form.get('emailaddress')
    subject = request.form.get('subject')
    elog = ElogForm(request.form)
    try:
        emailaddress = request.form.get('emailaddress')
    except Exception as e:
        emailaddress = 'steel.ricciotti@gmail.com'
    # sender = 'sricciotti@teppermans.com'
    # subject = "Logs for" 
    # to = emailaddress
    # names = ["Daily Logs"]
    # files = "/var/www/html/webapp/sendtomto.xlsx"
    # message_text = "Delivery Call Blast Results for deliveries occuring on " 
    # message = create_message_with_attachment(sender, to, subject, message_text, file = files)
    # if(len(str(emailaddress)) > 2):

    #     msg = Message("Subject", sender='steel.ricciotti@gmail.com', recipients=['steel.ricciotti@gmail.com'])
    #     msg.body = request.form.get('message')

    #     # with open("/var/www/html/webapp/sendtomto.xlsx", encoding = "utf-8") as fp:
    #     #     msg.attach("sendtomto.xlsx", "sendtomto.xlsx", fp.read(encoding = "utf-8"))          
    # mail.send(message)
    # if not current_user.is_authenticated:
    #     return redirect(url_for('admin.login_view'))

    # date = request.form.get('datefrom')
    elog = ElogForm(request.form)
    form = DriverForm(request.form)

    #     emailaddress = 1
    # try:
    #     date = request.form.get('datefrom')
    # except Exception as e:
    #     date = "2017-03-03"    
    # # date = "2017-03-03"
    # print(date)


    # #data = RPM.query.filter_by(user_id = current_user.get_id(), daterecorded = date).all()
    data = [1,2,3,4,5,6,7,8]
    xdata = []
    count = 0
    for i in data:
        xdata.append(count)
        count += 1
    #try:
    #this_driver = drivers.query.filter_by(user_id=1).all()
    this_driver = drivers.query.filter_by(user_id=current_user.get_id()).all()
    for i in this_driver:
        first_five = i.First_Name[:5]
        last_two_driver_license = i.Drivers_License[:-2]
        eighth_ninth = i.Drivers_License
        eighth_ninth_counter = 0
        for i in eighth_ninth:
            if(i.isnumeric()):
                eighth_ninth_counter = eighth_ninth_counter + int(i)
        eighth_ninth_counter = eighth_ninth_counter[:-2]
        tenth_to_fifteenth = arrow.now().format('MMDDYY')
        seventeenth_twenty_fifth = '000000000'


    if len(str(first_five) > 5):
        _len_counter = len(str(first_five))
        for i in range(0,int(len(_len_counter))):
            first_five.append('_')


    if(len(str(emailaddress)) > 2):
        linecounter = 0
        #This ensures that the correct row contains the data
        _linecountermapper_ = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        _line_counter_mapper_iteration_counter_ = 1
        filename = ("/var/www/html/webapp/sendtomto.xlsx")
        wb = openpyxl.load_workbook(filename)
        sheet = wb.get_sheet_by_name('Sheet1')
        sheet['A1'] = "ELD File Header Segment: <CR>"

        drivers_data_model = drivers.query.all()

        #Drivers data model
        if(linecounter > 25):
            _line_counter_mapper_iteration_counter_ += 1
        for i in drivers_data_model:
            linecounter += 1
            _temp_row_counter_ = ""
            for i in range(0, _line_counter_mapper_iteration_counter_):
                _temp_row_counter_ = _temp_row_counter_  + (_linecountermapper_[_line_counter_mapper_iteration_counter_])
            sheet[_temp_row_counter_ + '1'] = i.Last_Name
            sheet[_temp_row_counter_ + '2'] = i.First_Name
            sheet[_temp_row_counter_ + '3'] = i.ELD_Username
            sheet[_temp_row_counter_ + '4'] = i.Drivers_License_State
            sheet[_temp_row_counter_ + '5'] = i.Drivers_License
            sheet[_temp_row_counter_ + '6'] = "Checksum"


        for i in codrivers_data_model:
            linecounter += 1
            sheet['B1'] = i

        codrivers_data_model = codrivers.query.all()

        #Drivers data model
        if(linecounter > 25):
            _line_counter_mapper_iteration_counter_ += 1
        for i in codrivers_data_model:
            linecounter += 1
            _temp_row_counter_ = ""
            for j in range(0, _line_counter_mapper_iteration_counter_):
                _temp_row_counter_ = _temp_row_counter_  + (_linecountermapper_[_line_counter_mapper_iteration_counter_])
            sheet[_temp_row_counter_ + '1'] = i.Last_Name
            sheet[_temp_row_counter_ + '2'] = i.First_Name
            sheet[_temp_row_counter_ + '3'] = i.ELD_Username
            sheet[_temp_row_counter_ + '6'] = "Checksum"

        power_unit_number = truck.query.all()
        trailers = Trailers.query.filter_by(todays_log = todays_log).all()


        for i in power_unit_number:
            linecounter += 1
            _temp_row_counter_ = ""
            for j in range(0, _line_counter_mapper_iteration_counter_):
                _temp_row_counter_ = _temp_row_counter_  + (_linecountermapper_[_line_counter_mapper_iteration_counter_])

            sheet[_temp_row_counter_ + '1'] = i.unit
            sheet[_temp_row_counter_ + '2'] = i.VIN
            for j in trailers:
                trailersnumber = j.Unit + "," +  trailersnumber
            sheet[_temp_row_counter_ + '3'] = trailersnumber
            sheet[_temp_row_counter_ + '6'] = "Checksum"


        carrier_info = company.query.filter_by(user_id = current_user.get_id()).all()
        if(linecounter > 25):
            _line_counter_mapper_iteration_counter_ += 1

        for i in carrier_info:
            linecounter += 1
            sheet['D1'] = i
            _temp_row_counter_ = ""
            for j in range(0, _line_counter_mapper_iteration_counter_):
                _temp_row_counter_ = _temp_row_counter_  + (_linecountermapper_[_line_counter_mapper_iteration_counter_])
            sheet[_temp_row_counter_ + '1'] = i.USDOT
            sheet[_temp_row_counter_ + '2'] = i.companyname

            #Need Multiday-basis used
            sheet[_temp_row_counter_ + '3'] = "Multiday-basis used"
            sheet[_temp_row_counter_ + '6'] = "Checksum"

        for i in doocument_info:
            sheet['A'+_row_] = "Document Number"
            sheet['B' + _row_] = "Exempt Driver Configuration"
            sheet['C' + _row_] = "Line Data Check Value"

        _row_ += 1
        sheet['A' + _row_] = "Current Data"
        sheet['B' + _row_] = "Current Time"
        sheet['C' + _row_] = "Current Latitude"
        sheet['D' + _row_] = "Current Longitude"
        sheet['E' + _row_] = "Current Total Vehicle Miles"
        sheet['F' + _row_] = "Current Total Engine Miles"
        sheet['G' + _row_] = "Line Data Check Value"
        sheet['H' + _row_] = "<CR>"

        _row_ += 1
        sheet['A' + _row_] = "ELD Registration ID"
        sheet['B' + _row_] = "ELD Identifier"
        sheet['C' + _row_] = "ELD Authentication Value"
        sheet['D' + _row_] = "Output File Line Comment"
        sheet['E' + _row_] = "Line Data Check Value"
        sheet['F' + _row_] = "<CR>"

#4.8.2.1.3

#User List
        _truck_user_list_ = truck.query.filter_by(user_id = current_user.get_id(), )
        for _i_ in _truck_user_list_:
            sheet['A' + _row_] = "does not exist i.order_number"
            sheet['B' + _row_] = i.unit
            sheet['C' + _row_] = i.VIN
            sheet['D' + _row_] = "Line Data Check Value"
            sheet['E' + _row_] = "<CR>"
            _row_ += 1


        sheet['G1'] = "User List: <CR>"
        for i in user_list:
            sheet['H1'] = i
#CMV List
        sheet['A'+_row_] = "CMV List: <CR>"

        for i in cmv_list:
            sheet['I1'] = i
#Events List
#4.8.2.1.4
        _events_list_ = Events.query.filter(user_id = current_user.get_id(), Event_Type = 1, todays_log = '2122017')
        #_events_list_ = Events.query.filter(user_id=1, Event_Type=1, todays_log >= 2122017)

        for _i_ in _events_list_:
            sheet['A' + _row_] = i.Event_Sequence_ID_Number
            sheet['B' + _row_] = i.Event_Record_Status
            sheet['C' + _row_] = i.Event_Record_Origin
            sheet['D' + _row_] = i.Event_Type
            sheet['E' + _row_] = i.Event_Code
            sheet['F' + _row_] = i.Event_Date
            sheet['G' + _row_] = i.Event_Time
            sheet['H' + _row_] = i.Accumulated_Engine_Miles
            sheet['I' + _row_] = i.Elapsed_Engine_Hours
            sheet['J' + _row_] = i.Event_Latitude
            sheet['K' + _row_] = i.Event_Longitude
            sheet['L' + _row_] = i.Distance_Since_Last_Valid_Coordinates
            sheet['M' + _row_] = i.Event_Code
            sheet['N' + _row_] = i.Event_Code
            sheet['O' + _row_] = i.Malfunction_Indicator_Status
            sheet['P' + _row_] = i.Data_Diagnostic_Event_Indicator_Status
            sheet['Q' + _row_] = "Event Data Check Value"
            sheet['R' + _row_] = "Line Data Check Value"
            sheet['S' + _row_] = "<CR>"


        sheet['A' + _row] = "ELD Event Annotations or Comments:<CR>"
        _events_data_ = Events.guery.filter_by(user_id = current_user.get_id()).query()
        _comments_data_ = db.session.execute('select * from events where Event_Comment IS NOT NULL')
        for i in _comments_data_:
            sheet['A' + _row_] = i[0]
            sheet['B' + _row_] = i[1]
            sheet['C' + _row_] = i[2]
            sheet['D' + _row_] = i[3]
            sheet['E' + _row_] = i[4]
            sheet['F' + _row_] = i[5]
            sheet['G' + _row_] = i[6]


#Certifications Actions
        #Need to correct event type
        sheet['A' + _row] = "Driver's Certification/Recertification Actions:<CR>"
        _certification_events_data_ = Events.guery.filter_by(user_id=current_user.get_id(), event_type = 4).query()
        for i in _certification_events_data_:
            sheet['A' + _row_] = i.Event_Sequence_ID_Number
            sheet['B' + _row_] = i.Event_Code
            sheet['C' + _row_] = i.Event_Date
            sheet['D' + _row_] = i.Event_Time
            sheet['E' + _row_] = "Date"
            sheet['F' + _row_] = "Order Number"
            sheet['G' + _row_] = "Line Data Check Value"
            sheet['H' + _row_] = "<CR>"


        # Need to correct event type
        sheet['L1'] = "Malfunction and Data Diagnostic Events:<CR>"
        _certification_events_data_ = Events.guery.filter_by(user_id=current_user.get_id(), event_type=4).query()
        for i in _certification_events_data_:
            sheet['M1'] = i

        sheet['N1'] = "ELD Login/Logout Report:<CR>"
        # Need to correct event type
        _login_logout_events_data_ = Events.guery.filter_by(user_id=current_user.get_id(), event_type=4).query()
        for i in _login_logout_events_data_:
            sheet['A' + _row_] = i.Event_Sequence_ID_Number
            sheet['B' + _row_] = i.Event_Code
            sheet['C' + _row_] = "ELD Username"
            sheet['D' + _row_] = "ELD Username"



        sheet['P1'] = "CMV Engine Power-Up and Shut Down Activity:<CR>"
        # Need to correct event type
        _powerup_powerdown_events_data_ = Events.guery.filter_by(user_id=current_user.get_id(), event_type=5).query()
        for i in _powerup_powerdown_events_data_:
            sheet['Q1'] = i

        # Need to correct event type
        sheet['R1'] = "Unidentified Driver Profile Records:<CR>"
        _unidentified_driver_events_data_ = Events.guery.filter_by(user_id=current_user.get_id(), event_type=6).query()
        for i in _unidentified_driver_events_data_:
            sheet['S1'] = i
        sheet['T1'] = "End of File:<CR>"


        for row in sheet['A3:Q300']:
            for cell in row:
                cell.value = None
        #I think this will simply generate a text file that a C# webservice will then send off

        counter = 3
        for i in range(0, len(data)):
            print(data[i])
            try:
                (sheet['A' + str(counter)]) = str(data[i])
                (sheet['B' + str(counter)]) = str(xdata[i])
            except Exception as e:
                print(e)
            counter += 1
        wb.save(filename)
        day = datetime.datetime.today()
        today = datetime.date.today()
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        sender = 'sricciotti@teppermans.com'
        subject = "Logs for" + str(day.year) + "-" + str(day.month) + "-" + str(date)
        to = emailaddress
        names = ["Daily Logs"]
        files = "/var/www/html/webapp/sendtomto.xlsx"
        message_text = "Delivery Call Blast Results for deliveries occuring on " + str(day.year) + "-" + str(
            day.month) + "-" + str(day.day)
        message = create_message_with_attachment(sender, to, subject, message_text, file = files)
        SendMessage(service=service, user_id='me', message=message)

    return render_template('senddataemail.html',form=form, elog=elog, xdata = xdata, data = data)


@webservices_blueprint.route('/senddatabluetooth', methods = ['GET', 'POST'])
def SendDataBluetooth():
    # This code should present the user with the option to select a date and an email to send and then transmit
    # the logs over email. Something like
    ####
    # Hello, please enter the email address
    #Next Page---Thank- your logs are on their way...I will need a form and a button. This server side code will
    # contain the GMAIL credentials. Perhaps we require an elogstation  domain? Can I use wtforms or do I require bootstrap
    #
    #
    bluetooth = BluetoothServicesForm()
    bluetooth = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatabluetooth.html',data = bluetooth)



@webservices_blueprint.route('/senddatawifi', methods = ['GET', 'POST'])
def SendDataWifi():
    wifiservice = WIFIservicesForm()
    emailaddress = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatawifi.html',data= wifiservice)




@webservices_blueprint.route('/senddatausb', methods = ['GET', 'POST'])
def SendDataUSB():
    usbservice = USBServicesForm()
    emailaddress = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatausb.html',data= usbservice)