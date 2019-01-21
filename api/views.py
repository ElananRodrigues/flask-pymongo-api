from flask import Flask, jsonify, request, url_for, redirect
import datetime
import json

from .models import ClientMongoModel, ObjectId
from .serializers import estudantes

err = {'count': 0,'response': "Nenhum dado encontrado"}

class Api():

	def find(self, string, page, req=""):

		search = self.switch(string, req)

		try:
			model = ClientMongoModel()
			query = model.db().find(search).skip((page-1)*20).limit(20)
			
			response = self.searchAll(query)
			return response, 200

		except:
			return (err), 400


	def create(self, req=""):
		
		estudante = req.args.to_dict()

		try:
			model = ClientMongoModel()
			query = estudante

			response = model.db().insert_one(query)
			return response, 201

		except:
			return (err), 400


	def delete(self, req=""):
		
		ra = req.args.get('ra', None)
		campus = req.args.get('campus', None)

		search = {"ra": ra, "campus": campus}

		try:
			model = ClientMongoModel()
			query = model.db().find_one(search)
			estudante = self.search(query)

			response = model.db().delete_one(estudante)
			return response, 200

		except:
			return (err), 400


	def switch(self, string, req):
		
		if string == "modalidade":
			search = self.modalidade(req)
		elif string == "campus":
			search = self.campus(req)
		else:
			search = {}

		return search


	def campus(self, req):

		campus = req.args.get('place', None)
		start = req.args.get('start', None)
		end = req.args.get('end', None)

		if start and end:
			data = { "$and": 
				[
					{ 'campus': { "$regex": ".*" + campus + ".*", "$options": "-i" } },
					{ 'data_inicio': {'$gte': start, '$lt': end} }
				]
			}
		else:
			data = { 'campus': { "$regex": ".*" + campus + ".*", "$options": "-i" } }

		return data


	def modalidade(self, req):

		mod = req.args.get('m', None)
		start = req.args.get('start', None)
		end = req.args.get('end', None)

		if start and end:
			data = { "$and": 
				[
					{ 'modalidade': {"$regex": ".*" + mod + ".*", "$options": "-i" }},
					{ 'data_inicio': {'$gte': start, '$lt': end}}
				]
			}
		else: 
			data = { 'modalidade': {"$regex": ".*" + mod + ".*", "$options": "-i" }}
		
		return data


	def search(self, string):

		response = estudantes(string)
		return ({'response': response})


	def searchAll(self, query):

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

			
	def urls(self,hosts):

		return ([{
			"api":{
					'search': {
						'modalidade': hosts+'/estudantes/page/1/search/modalidade?m=PRESENCIAL&start=2014-01-01&end=2014-02-30',
						'campus': hosts+'/estudantes/page/1/search/campus?place=AQ',
						'campus_date': hosts+'/estudantes/page/1/search/campus?place=AQ&start=2014-01-01&end=2014-02-30'
					},
					'post':{
						'create': hosts+'/estudantes/create?idade=22.0&nivel_do_curso=TECNOLOGIA&ra=7777.0&modalidade=PRESENCIAL&nome=Robo&curso=Teste&campus=LA&municipio=Curitiba&data_inicio=2019-01-20'
					},
					'delete':{
						'RA': hosts+'/estudantes/delete?RA=7777.0&campus=LA'
					}
				}
			}])