#!/usr/bin/env python

import sys
import pandas as pd
from pymongo import MongoClient
import json
import os

def import_content(filepath):

    db = MongoClient("mongodb://localhost:27017/")['base']['estudantes'] 

    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))

    db.remove()
    db.insert(data_json)

    print("Dados inseridos !")

if __name__ == "__main__":
  filepath = 'dataset_estudantes.csv'
  # import_content(filepath)