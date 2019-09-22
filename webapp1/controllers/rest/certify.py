from flask.ext.restful import Resource
from flask import abort, current_app
from webapp1.models import User, RPM, db, Events
from .parsers2 import eld_post_parser, user_data_parser, eld_get_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from flask import abort
from flask.ext.restful import Resource, fields, marshal_with
from .fields import HTMLField
from flask.ext.login import current_user
import datetime
eld_fields = {
	'user_id':fields.Integer()
}
#Need to determine whether the API will control the events or whether this will be entered into an intermediary table.
#Likely should simply be an event. Need to add

class CertifyAPI(Resource):
	@marshal_with(eld_fields)
	def get(self):
		args = eld_post_parser.parse_args()

		# newdata = str(data).split(",")
		# allnewdata = []
		# for i in range(0, len(data), 6):
		# 	thisvalue = data[i:i+5]
		#     newdata = {'Event_Time': thisvalue[0], 'Event_Latitude': thisvalue[1], 'Event_Longitude': thisvalue[2],   'Odometer': thisvalue[3], 'Elapsed_Engine_Hours': thisvalue[4],'Event_Type': thisvalue[5]}
		# def post(self):
    #     args = user_post_parser.parse_args()
    #     args = user_post_parser.parse_args()
    #     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()

    #     if user.check_password(args['password']):
    #         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
    #         return {"token": s.dumps({'id': user.id})}
    #     else:
    #         abort(401)
		return {"result": args}

	def post(self):
		args = eld_post_parser.parse_args()

		data = str(datetime.datetime.today().day) + "" + str(datetime.datetime.today().month) + "" + str(
			datetime.datetime.today().year)
		thisdate_ = int(data)
		previousmax = db.engine.execute(
			'select max("Event_Code") from events where events.todays_log = %s and user_id = %s',[int(data), args['user_id']])
		try:
			for i in previousmax:
				data = i
				data = data[0]
			if (int(data) > 8):
				eventrecord = 9
			else:
				eventrecord = data + 1
		except Exception as e:
			eventrecord = 1
		event = Events(Event_Record_Status=1, Event_Record_Origin=2, Event_Type=4, Event_Code=int(eventrecord),
					   Event_Date=datetime.datetime.now(), Event_Time=datetime.datetime.now(),
					   user_id=args['user_id'], todays_log=thisdate_)
		db.session.add(event)
		db.session.commit()
		update = "Logs Have Been Certified for the " + str(eventrecord) + "time"
		return {"result": update}