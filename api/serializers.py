
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