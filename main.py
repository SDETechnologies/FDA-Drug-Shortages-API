import flask
import requests
import json
import urllib.request
import openpyxl
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
from flask_cors import CORS, cross_origin

DATA_FILE_NAME = 'data'
DATA_FILE_TYPE = 'csv'
# DATA_FILE_TYPE = 'xlsx'
DATA_FILE_NAME_WHOLE = DATA_FILE_NAME + '.' + DATA_FILE_TYPE

DATA_FILE_ROW_COUNT = 22

app = Flask(__name__)
api = Api(app)
cors = CORS()
cors = CORS(app, resources={r"/*": {"origins": "https://rxbuddy.net"}})
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3005"}})

def getStatus(df, row):
    return df.loc[row][11]

def getCurrentRows(df):
    return df.loc[df[' Status'] == 'Current']
    

def getCurrentGenericShortages(df):
    currentRows = getCurrentRows(df)
    return currentRows['Generic Name'].unique().tolist()

def getDF():
    df = pd.read_csv(DATA_FILE_NAME_WHOLE)
    return df

def getData():
    # response = requests.get('https://www.accessdata.fda.gov/scripts/drugshortages/Drugshortages.cfm')
    # print(response.json)
    urllib.request.urlretrieve('https://www.accessdata.fda.gov/scripts/drugshortages/Drugshortages.cfm',DATA_FILE_NAME_WHOLE)

class CurrentGeneric(Resource):
        def get(self):
            currentGenericDrugs = getCurrentGenericShortages(df)
            currentRows = getCurrentRows(df)
            # return json.dumps(currentRows.values.tolist())
            return currentGenericDrugs

api.add_resource(CurrentGeneric, '/currentgeneric')

getData()
df = getDF()
# print('df: ', df)
# test = getStatus(df, 1)
# print('test: ', test)
test = getCurrentGenericShortages(df)

print('---------------------------------------')

if __name__ == '__main__':
    app.run()  # run our Flask app