
##This module inserts an event record every hour if a previous event has not run in an hour

import pdb
from flask import Flask
import time
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, DateTime, CHAR, Time
from models import company, RPM, db, drivers, Events
from random import randint
app = Flask(__name__)
import psycopg2
import time
import datetime
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost/elogstation4')
connection = engine.connect()

# conn = psycopg2.connect('postgresql://postgres:postgres@localhost/elogstation4')
# cur = conn.cursor()
# cur.execute("select * from Events;")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/elogstation4'
db.init_app(app)
minutehand = 0
hourhand = 0

        # self.date = date
today = datetime.date.today()        


with app.app_context():
    while True:
        users = connection.execute('select id from elogstation4.public.user')
        todays_log = str(datetime.datetime.now().day) + "" + str(datetime.datetime.now().month) + "" + str(
            datetime.datetime.now().year)
        for i in users:
            user_id = i[0]
            print(i)
            device_id_ = connection.execute('select "device_id" from drivers where user_id = %s', i[0])
            for i in device_id_:
                device_id = i[0]
                print(i)


            current_status = connection.execute('select "Current_Status" from drivers where user_id = %s', i[0])
            for i in current_status:
                driver_status = (i[0])

            result = connection.execute('select max("Event_Date") from Events where user_id = %s;', [i[0]])
            for i in result:
                olddate = i[0]

            hours = (datetime.datetime.now() - olddate)
            if ((hours.seconds / 3600) > 1):
                print("Execute Logs")
                neweventsobject_ = Events(Event_Record_Status = 1, Event_Record_Origin = 1,Event_Type = 1, Event_Code = driver_status,Event_Date = datetime.datetime.now(),Event_Time = datetime.datetime.now(), user_id = user_id , device_id = device_id, todays_log = todays_log)
                db.session.add(neweventsobject_)
                db.session.commit()

        time.sleep(15)