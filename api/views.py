from flask import Flask, jsonify, request, url_for, redirect

from .models import db, ObjectId
from .serializers import estudantes

err = {'count': 0,'response': "Nenhum dado encontrado"}

def getId(id):

	if not id:
		return (err), 400
	else:
		try:
			query = db.find_one(dict(_id=ObjectId(str(id))))
			response = search(query)
			return response, 200
		except:
			return (err), 400

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
		return  (err), 400


def getAll(string, page):

	try:
		query = db.find({}).skip((page-1)*20).limit(20)
		response = searchAll(query)
		return response
	except: 
		return ["Nenhum dado encontrado"], 400


def search(string):

	response = estudantes(string)
	return ({'response': response})


def searchAll(query):

	count = 0
	pages = 0
	response = []

	if query.count() > 0:
		for string in query:
			response.append(estudantes(string))

		count = query.count()
		pages = int((count/20))

		return ({'count': count,'pages': pages,'response': response})
	else:
		return ({'count': count,'pages': pages,'response': "Nenhum dado encontrado"})

		
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