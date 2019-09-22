ListOfLoggedIn = {'device':[{'number':'name'},{'driver':'name'},{'status':'name'}]}
print(ListOfLoggedIn['device'][0]['number'])

_list_ = {}
data = {'device':{'number':101,'status':'on',	'driver':'bob',	'name':'1010'	}}
data['device']['number'] = '1'
_list_['1'] = data
print(_list_['1']['device']['number'])

#ListOfLoggedIn = {'device':{'number':'name'},{'driver':'name'},{'status':'name'}}
ListOfLoggedIn = {}
device = db.session.query(Device.Device_Number, Device.driver_id, Device.status).all()
from collections import namedtuple
named_device = []
name_id_status = namedtuple("Name_ID_Status",["Device_Number","driver_id","status"])
for named_data in device:
	namedPi = name_id_status(*named_data)
	named_device.append(namedPi)

for i in range(len(named_device)):
	if(named_device[i].driver_id != None):
		data = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = named_device[i].driver_id).all()
		try:
			named_device[i] = named_device[i]._replace(driver_id = data[0][0] + " " + data[0][1])
		except Exception as e:
			named_device[i] = named_device[i]._replace(driver_id ="John Doe")


for i in named_device:
	if (i.driver_id != None):
		data = db.session.query(drivers.First_Name, drivers.Last_Name).filter_by(uid = i.driver_id).all()
		try:
			i.driver_id = data[0][0] + " " + data[0][1]
		except Exception as e:
			i.driver_id = ""
