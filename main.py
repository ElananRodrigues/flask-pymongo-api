from flask_api import FlaskAPI, status, exceptions
from api.views import getId, getString, getAll, urls, request, url_for, redirect

app = FlaskAPI(__name__)

@app.route('/estudantes/user/id/<id>/', defaults=None)
@app.route('/estudantes/user/id/<id>', methods=['GET'], defaults=None)
def id(id):
	return getId(id)

@app.route('/estudantes/page/<int:page>/search/<string>/', defaults=None)
@app.route('/estudantes/page/<int:page>/search/<string>', methods=['GET'], defaults=None)
def string(string, page):
	return getString(string, page)

@app.route('/estudantes/page/<int:page>/search/', methods=['GET'],defaults=None)
def all(page):
	return getAll(page)

@app.route('/<page>/<url>/<text>/', methods=['GET'], defaults=None)
def notFound(page,url,text):
	return redirect('/')

@app.route('/', methods=['GET'], defaults=None)
def index():
	hosts = request.host_url.rstrip('/')
	return urls(hosts)


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000)