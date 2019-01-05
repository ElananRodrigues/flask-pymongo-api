from flask import request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)
db = MongoClient("mongodb://localhost:27017/")['base']['estudantes']

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

	return ({'response': response})


def searchAll(query):

	count = 0
	pages = 0
	response = []

	for string in query:
		response.append(estudantes(string))

	count = query.count()
	pages = int((count/20))

	return ({'count': count,'pages': pages,'response': response})


@app.route('/estudantes/id/<id>', methods=['GET'])
def getId(id):
	try:
		query = db.find_one(dict(_id=ObjectId(str(id))))
		response = search(query)
		return response, 200
	except:
		return ["Nenhum dado encontrado"], 400


@app.route('/estudantes/page/<int:page>/search/<string>', methods=['GET'])
def getString(string, page):

	string = ''.join(c for c in string if c not in '?&:$"%!/;|()=`´')
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

		print(query)

		response = searchAll(query)
		return response, 200
	except:
		return ["Nenhum dado encontrado"], 400


@app.route('/estudantes/page/<int:page>', methods=['GET'])
def get(page):
	try:
		query = db.find({}).skip((page-1)*20).limit(20)
		response = searchAll(query)
		return response
	except: 
		return []

@app.route('/', methods=['GET'])
def index():

	return {
		'page': '/estudantes/page/1',
		'id': '/estudantes/id/id',
		'search': {
			'nome': '/estudantes/page/1/search/ALESSANDRA',
			'campus': '/estudantes/page/1/search/AQ',
			'curso': '/estudantes/page/1/search/ESPECIALIZAÇÃO',
			'modalidade': '/estudantes/page/1/search/PRESENCIAL',
			'municipio': '/estudantes/page/1/search/Aquidauana',
			'nivel_do_curso': '/estudantes/page/1/search/INTEGRADO'
		}
	}


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000, debug=True)