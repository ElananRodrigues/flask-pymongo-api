from flask_api import FlaskAPI, status, exceptions
from api.views import request, url_for, redirect, Api
app = FlaskAPI(__name__)

@app.route('/estudantes/page/<int:page>/search/<string>', methods=['GET'], defaults=None)
def get(string, page):
	api = Api()
	return api.find(string, page, request)

@app.route('/estudantes/create', methods=['GET','POST'], defaults=None)
def post():
	api = Api()
	return api.create(request)

@app.route('/estudantes/delete', methods=['GET','DELETE'], defaults=None)
def drop():
	api = Api()
	return api.delete(request)

@app.route('/', methods=['GET'], defaults=None)
def index():
	hosts = request.host_url.rstrip('/')
	api = Api()

	return api.urls(hosts)


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000)