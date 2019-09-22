from flask.ext.restful import Resource
from flask import abort, current_app
from webapp1.models import User, RPM, db, Events
from .parsers2 import eld_post_parser, user_data_parser, eld_get_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from flask import abort
from flask.ext.restful import Resource, fields, marshal_with
from .fields import HTMLField
import datetime
from flask.ext.login import current_user
eld_fields = {
	'user_id':fields.Integer(),
	'status':fields.Integer()
}
#Need to determine whether the API will control the events or whether this will be entered into an intermediary table.
#Likely should simply be an event. Need to add

class StatusAPI(Resource):
	@marshal_with(eld_fields)
	def get(self):
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
		return {"result": args}

	def post(self):
		args = eld_post_parser.parse_args()
		db.engine.execute('update drivers set "Current_Status" = %s where user_id = %s', [int(args['status']), int(args['user_id'])])
		todaysdate_ = str(str(datetime.datetime.today().day)) + "" + str(datetime.datetime.today().month) + "" + str(datetime.datetime.today().year)
		event = Events(Event_Record_Status=1, Event_Record_Origin=2, Event_Type=3, Event_Code=int(args['status']),
					   Event_Date=datetime.datetime.now(), Event_Time=datetime.datetime.now(),
					   user_id =int(args['user_id']), todays_log=todaysdate_)
		db.session.add(event)
		db.session.commit()
		return {"result": "Success"}