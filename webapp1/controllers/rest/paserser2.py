from flask.ext.restful import reqparse

user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('username', type=str, required=True)
user_data_parser.add_argument('password', type=str, required=True)

eld_get_parser = reqparse.RequestParser()
eld_get_parser.add_argument('page', type=int, location=['args', 'headers'])
eld_get_parser.add_argument('user', type=str, location=['args', 'headers'])

eld_post_parser = reqparse.RequestParser()
eld_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth token is required to submit data"
)
eld_post_parser.add_argument(
    'date',
    type=date,
    required=True,
    help="Need time of day"
)

eld_post_parser.add_argument(
    'todays_date',
    type=int,
    required=False,
    help="Need todays date in format of DDMMYYY"
)

eld_post_parser.add_argument(
    'this_id',
    type=int,
    required=False,
    help="Need todays date in format of DDMMYYY"
)

eld_post_parser.add_argument(
    'longitude',
    type=int,
    required=True,
    help="Need current longitude"
)
eld_post_parser.add_argument(
    'latitude',
    type=int,
    action='append'
)


eld_post_parser.add_argument(
    'rpm',
    type=int,
    action='append'
)


eld_post_parser.add_argument(
    'user_id',
    type=int,
    action='append'
)


#Not sure yet whether I will be sending the user_id and/or  the company id
eld_post_parser.add_argument(
    'user_id',
    type=int,
    action='append'
)