from flask import Flask, jsonify, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

db = MongoClient("mongodb://localhost:27017/")['base']['estudantes']

err = {'count': 0,'response': "Nenhum dado encontrado"}

def urls(hosts):

	return ([{
		"api":{
				'id': hosts+'/estudantes/user/id/5c30285fc34fcf2f31303a9c',
				'search': {
					'nome': hosts+'/estudantes/page/1/search/Alessandra',
					'campus': hosts+'/estudantes/page/1/search/Aq',
					'curso': hosts+'/estudantes/page/1/search/Computador',
					'modalidade': hosts+'/estudantes/page/1/search/Presencial',
					'municipio': hosts+'/estudantes/page/1/search/Aquidauana',
					'nivel_do_curso': hosts+'/estudantes/page/1/search/Integrado'
				}
			}
		}])

def estudantes(string):
	
	estudantes = { 
		"_id": str(string['_id']),
		"nome" : string['nome'],
	    "curso" : string['curso'],
	    "idade" : string['idade'],
	    "nivel_do_curso" : string['nivel_do_curso'],
	    "ra" : string['ra'],
	    "modalidade" : string['modalidade'],
	    "campus" : string['campus'],
	    "municipio" : string['municipio'],
	    "data_inicio" : string['data_inicio']
	}

	return estudantes


def search(string):

	response = estudantes(string)
	return jsonify({'response': response})


def searchAll(query):

	count = 0
	pages = 0
	response = []

	if query.count() > 0:
		for string in query:
			response.append(estudantes(string))

		count = query.count()
		pages = int((count/20))

		return jsonify({'count': count,'pages': pages,'response': response})
	else:
		return jsonify({'count': count,'pages': pages,'response': "Nenhum dado encontrado"})


@app.route('/estudantes/user/id/<id>/', defaults=None)
@app.route('/estudantes/user/id/<id>', methods=['GET'], defaults=None)
def getId(id):
	if not id:
		return jsonify(err), 400
	else:
		try:
			query = db.find_one(dict(_id=ObjectId(str(id))))
			response = search(query)
			return response, 200
		except:
			return jsonify(err), 400
		
	

@app.route('/estudantes/page/<int:page>/search/<string>/', defaults=None)
@app.route('/estudantes/page/<int:page>/search/<string>', methods=['GET'], defaults=None)
def getString(string, page):

	try:
		query = db.find({
			"$or":  
			[
	    		{ 'nome' : {"$regex": ".*" + string + ".*", "$options": "-i"}},
	    		{ 'campus' : {"$regex": ".*" + string + ".*", "$options": "-i" }},
	    		{ 'curso' : {"$regex": ".*" + string + ".*", "$options": "-i" }},
	    		{ 'modalidade' :{"$regex": ".*" + string + ".*", "$options": "-i" }},
	    		{ 'municipio' :{"$regex": ".*" + string + ".*", "$options": "-i" }},
	    		{ 'nivel_do_curso' :{"$regex": ".*" + string + ".*", "$options": "-i" }}
			]
		}).skip((page-1)*20).limit(20)

		response = searchAll(query)
		return response, 200
	except:
		return  jsonify(err), 400


@app.route('/estudantes/page/<int:page>/search/', methods=['GET'],defaults=None)
def errorPage(page):
	try:
		query = db.find({}).skip((page-1)*20).limit(20)
		response = searchAll(query)
		return response
	except: 
		return ["Nenhum dado encontrado"], 400

@app.route('/<page>/<url>/<text>/', methods=['GET'], defaults=None)
def notFound(page,url,text):
	return redirect('/')

@app.route('/', methods=['GET'], defaults=None)
def index():
	hosts = request.host_url.rstrip('/')
	return urls(hosts)


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000)