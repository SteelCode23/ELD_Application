from flask import abort, current_app
from flask.ext.restful import Resource
from webapp1.models import User
from .parsers import user_post_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeSerializer
import json

def create_serializer():
    return Serializer(current_app.config['SECRET_KEY'],  expires_in=604800)

class AuthApi(Resource):
    def post(self):
        #SELECT LOGS FOR CURRENT USER
        args = user_post_parser.parse_args()
        print(args)
        #SELECT LOGS FOR CURRENT DATE
        try:
            user = User.query.filter_by(email=args['username']).one()

        except Exception as e:
            print(e)
        #SELECT LATITUDE

        #SELECT LONGITUDE

        #SELECT RPMS

        # if user.check_password(args['password']):
        print(current_app.config['SECRET_KEY'])
        try:
            s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
            # s = URLSafeSerializer(current_app.config['SECRET_KEY'])
            # s = URLSafeSerializer('736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b')

        except Exception as e:
            s = '103f3'

        print(s.dumps({'id': user.id}))
        # s.loads(str(datacontent.content).split(':')[1].split('"')[1])['id']

        try:
            return {"user_id":user.id,"token": s.dumps({'id': user.id}).decode('utf-8')}
        except Exception as e:
            return {"token": s}
        # return (s)
        # else:
            # abort(401)
