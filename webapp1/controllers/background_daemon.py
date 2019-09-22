#This is the background daemon that constantly updates the database with the data that the ELD is streaming
import time
from webapp1.models import drivers, db, RPM, User, Events
driverstatuses = db.engine.execute("select * from drivers")
for i in driverstatuses:
    print(i)
    #Not sure why this is not working
    #Seems to be broken because of UID,
    newstatus = RPM(driver_id = i[0], status = i[7])
    print(db.session.add(newstatus))
    db.session.commit()    
    print(newstatus)
    event = Events(Event_Record_Status = 1, Event_Record_Origin = 2, Event_Type = 1, Event_Code = 3, Event_Date = 1, Event_Time = datetime.datetime.now())
time.sleep(15)