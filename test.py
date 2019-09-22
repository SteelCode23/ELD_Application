import psycopg2
import time
import datetime
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost/elogstation4')
connection = engine.connect()

# conn = psycopg2.connect('postgresql://postgres:postgres@localhost/elogstation4')
# cur = conn.cursor()
# cur.execute("select * from Events;")
users = connection.execute('select id from elogstation4.public.user')
for i in users:
    current_status= connection.execute('select "Current_Status" from drivers where user_id = %s', i[0])
    for i in current_status:
        print(i[0])
    result = connection.execute('select max("Event_Date") from Events where user_id = %s;',[i[0]])
    for i in result:
        olddate = i[0]
        print(olddate)
    hours = (datetime.datetime.now() - olddate)
    if((hours.seconds/3600) > 1):
        print("Execute Logs")