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
	'device_id':fields.Integer(),
	'rpm': fields.Integer(),
    'Event_Code': fields.Integer(),
    'rpm': fields.Integer(),
    'rpm': fields.Integer(),
	# 'daterecorded':fields.DateTime(dt_format='rfc822'),
	'longitude':fields.Float(),
	'speed':fields.Float(),
	'vehicle_miles':fields.Float(),
	'latitude':fields.Float(),
    'vin':fields.Float(),
    'Odometer':fields.Float(),
    'Engine_Hours':fields.Float(),
}
#Need to determine whether the API will control the events or whether this will be entered into an intermediary table.
#Likely should simply be an event. Need to add

class ELDAPI(Resource):
	@marshal_with(eld_fields)
	def get(self):
		# args = eld_post_parser.parse_args()
		# data = RPM.query.filter_by(user_id=current_user.get_id(), daterecorded=args['date']).all()
		date = "2016-07-07"

		data = RPM.query.filter_by(user_id=current_user.get_id(), daterecorded=date).all()
		    # def post(self):
    #     args = user_post_parser.parse_args()
    #     args = user_post_parser.parse_args()
    #     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()

    #     if user.check_password(args['password']):
    #         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
    #         return {"token": s.dumps({'id': user.id})}
    #     else:
    #         abort(401)
		return data

	def post(self):
		args = eld_post_parser.parse_args()
		user = User.verify_auth_token(args['token'])
		if not user:
			abort(401)
		else:
			print("Success")
		print(args)
		try:
			latitude = args['latitude'][0]
		except Exception as e:
			latitude = 0
		try:
			rpm = args['rpm'][0]
		except Exception as e:
			rpm = 0

		vehiclemiles = args['vehicle_miles']
		engine_hours = args['engine_hours']
		vin = args['vin']
		rpm = RPM(company_id=args['company_id'], user_id=args['user_id'], rpm=rpm, longitude=args['longitude'], latitude=latitude)
		db.session.add(rpm)
		db.session.commit()
		return {"result":args}