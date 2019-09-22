from flask.ext.restful import Resource
from flask import abort, current_app
from webapp1.models import User, RPM, db, Events,Locations_Specific_To_Driver
from .parsers2 import eld_post_parser, user_data_parser, eld_get_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
#import arrow
from flask import abort
from flask.ext.restful import Resource, fields, marshal_with
from .fields import HTMLField

from flask.ext.login import current_user
eld_fields = {
	'user_id':fields.Integer(),
	'device_id':fields.Integer(),
	'rpm': fields.Integer(),
    'this_id':fields.Integer(),
    'Event_Code': fields.Integer(),
    'rpm': fields.Integer(),
	# 'daterecorded':fields.DateTime(dt_format='rfc822'),
    'latitude':fields.Float(),
	'longitude':fields.Float(),
	'speed':fields.Float(),
	'vehicle_miles':fields.Float(),
    'vin':fields.Float(),
    'Odometer':fields.Float(),
    'Engine_Hours':fields.Float(),

}
#Need to determine whether the API will control the events or whether this will be entered into an intermediary table.
#Likely should simply be an event. Need to add

class GetLocationsAPI(Resource):
	@marshal_with(eld_fields)
	def get(self):
		args = eld_post_parser.parse_args()
    #     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()

    #     if user.check_password(args['password']):
    #         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
    #         return {"token": s.dumps({'id': user.id})}
    #     else:
    #         abort(401)
		#data = Locations_Specific_To_Driver.query.filter_by(user_id=args['user_id'], todaysdate=args['todaysdate']).all()
		data = Locations_Specific_To_Driver.query.filter_by(user_id=args['user_id'],this_id ='12102017').all()
		newlist_ = []
		for i in data:
			thisvalue = str(i).split(",")
			newdata = {'User_id': thisvalue[0], 'Longitude': thisvalue[1], 'Latitude': thisvalue[2],'Date': thisvalue[3]}
			newlist_.append(newdata)

		return {"result":newlist_}

	def post(self):
		args = eld_post_parser.parse_args()
		#     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()

		#     if user.check_password(args['password']):
		#         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
		#         return {"token": s.dumps({'id': user.id})}
		#     else:
		#         abort(401)
		# data = Locations_Specific_To_Driver.query.filter_by(user_id=args['user_id'], todaysdate=args['todaysdate']).all()
		# try:
		# 	data = Locations_Specific_To_Driver.query.filter_by(user_id=args['user_id'], todays_date=args['this_id']).all()
		# 	newlist_ = []
		# 	for i in data:
		# 		thisvalue = str(i).split(",")
		# 		newdata = {'User_id': thisvalue[0], 'Longitude': thisvalue[1], 'Latitude': thisvalue[2], 'Date': thisvalue[3]}
		# 		newlist_.append(newdata)
		# except Exception as e:
		data = Locations_Specific_To_Driver.query.filter_by(user_id=args['user_id'], todays_date=str(datetime.datetime.today().day) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)).all()
		newlist_ = []
		for i in data:
			thisvalue = str(i).split(",")
			newdata = {'User_id': thisvalue[0], 'Longitude': thisvalue[1], 'Latitude': thisvalue[2], 'Date': thisvalue[3]}
			newlist_.append(newdata)
		return {"result": newlist_}