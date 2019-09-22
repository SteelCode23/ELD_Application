try:
    from extensions import celery
except Exception as e:
    print(e)
try:
    from webapp1.extensions import celery
    from webapp1.models import db, Events
except Exception as e:
    print(e)
from celery import Celery
import datetime
app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend  = 'redis://127.0.0.1:6379/0')

@app.task
def add(x, y):
    return x + y

@celery.task()
def echo(msg):
    return msg

@celery.task()
def log(msg):
    event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 3, Event_Date = datetime.datetime.now(), Event_Time = datetime.datetime.now())
    db.session.add(event)
    db.session.commit()
    return msg