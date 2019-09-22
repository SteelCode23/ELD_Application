from flask.ext.restful import Resource


class PostAPI(Resource):
	def get(self):
		return {"result":"Post"}