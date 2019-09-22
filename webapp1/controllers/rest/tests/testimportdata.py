import pdb
from flask import Flask
import time
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, DateTime, CHAR, Time
from models import company, RPM, db
db = SQLAlchemy()
from random import randint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/elogstation'
db.init_app(app)

minutehand = 0
hourhand = 0

        # self.date = date
today = datetime.date.today()        
# day = today + datetime.timedelta(days=negativedays)
import datetime
today = datetime.date.today()        


with app.app_context():
    db.create_all()
    hourhand = 1    
    for j in range(0,762):
        for i in range(0,100):
            if(minutehand == 4):
                minutehand = 0
                hourhand += 1    
            minutes = minutehand * 15
            try:
                t = time(hourhand, minutes)
            except Exception as e:
                t = "01:00:00"
                print(e)
            negativedays = 0 - int(j)
            thisdate = today + datetime.timedelta(days=negativedays)
            print(thisdate)

            minutehand +=1
            rpm = RPM(company_id = 1, user_id = 2, rpm = randint(0,1000), longitude = 10021, latitude = 106156, datetimestamp = str(t), daterecorded = thisdate)
            with app.app_context():
                db.session.add(rpm)
                db.session.commit()
        negativedays = 0 - int(j)
        thisdate = today + datetime.timedelta(days=negativedays)
        print(thisdate)