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
eld_fields = {
	'user_id':fields.Integer(),
	'todayslog':fields.Integer()
}
#Need to determine whether the API will control the events or whether this will be entered into an intermediary table.
#Likely should simply be an event. Need to add

class EventsAPI(Resource):
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
		data = Events.query.filter_by(user_id=args['user_id'], todays_log=args['todayslog']).all()
		# def post(self):
		#     args = user_post_parser.parse_args()
		#     args = user_post_parser.parse_args()
		#     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()
		#     if user.check_password(args['password']):
		#         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
		#         return {"token": s.dumps({'id': user.id})}
		#     else:
		#         abort(401)
		data = Events.query.filter_by(user_id=args['user_id'], todays_log=args['todayslog']).all()
		newlist_ = []
		for i in data:
			thisvalue = str(i).split(",")
			newdata = {'Event_Time': thisvalue[0], 'Event_Latitude': thisvalue[1], 'Event_Longitude': thisvalue[2],'Odometer': thisvalue[3], 'Elapsed_Engine_Hours': thisvalue[4], 'Event_Type': thisvalue[5], 'Event_Code':thisvalue[6]}
			newlist_.append(newdata)
		return {"result": newlist_}