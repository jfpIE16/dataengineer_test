import os
import pandas as pd
import pymongo
import json
from google.cloud import firestore

def push_data_local(filepath, db_url, db_name, db_collection):
    myclient = pymongo.MongoClient(db_url, 27017)
    mydb = myclient[db_name]
    mycol = mydb[db_collection]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    mycol.delete_many({})
    mycol.insert_many(data_json)

def push_data_firebase(filepath):
    db = firestore.Client()
    doc_ref = db.collection(u'test_bam')
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))

    for datum in data_json:
        doc_ref.add(datum)


if __name__ == "__main__":
    filepath = './data/datos_base_clientes.csv'
    push_data_firebase(filepath)
    #push_data(filepath, 'localhost', 'test', 'test_bam')


