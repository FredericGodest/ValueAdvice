from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import webbrowser
import os
import json
import pandas as pd
import numpy as np
from wallstreet import Stock
import pickle
from Data import Update, UpdateTranspose
from Historic import DATA
import json

from flask_restful import Resource, request, Api #import request from flask restful

#Fonction Perso
def scale(table):
    #table["Capital"]=table["Capital"] / 1000000
    table["Evolution CA %"]=np.round(table["Evolution CA %"] * 100, 2)
    table["Evolution Rslt net %"]=np.round(table["Evolution Rslt net %"] * 100, 2)
    table["Evolution Benef %"]=np.round(table["Evolution Benef %"] * 100, 2)
    table["Marge Brute"]=np.round(table["Marge Brute"] * 100, 2)
    table["Evolution Marge %"]=np.round(table["Evolution Marge %"] * 100, 2)
    table["Resultat net/CA"]=np.round(table["Resultat net/CA"] * 100, 2)
    table["Charge/CA"]=np.round(table["Charge/CA"] * 100, 2)
    table["Evolution BPA %"]=np.round(table["Evolution BPA %"] * 100, 2)
    table["Evolution Dividende %"]=np.round(table["Evolution Dividende %"] * 100, 2)
    table["rendement dividende"]=np.round(table["rendement dividende"] * 100, 2)
    table["Payout Ratio"]=np.round(table["Payout Ratio"] * 100, 2)
    table["Evolution ROE"]=np.round(table["Evolution ROE"] * 100, 2)
    table["ROE"]=np.round(table["ROE"] * 100, 2)
    table["Evolution flux tréso"]=np.round(table["Evolution flux tréso"] * 100, 2)
    table["rendement / 5 ans"]=np.round(table["rendement / 5 ans"], 2)

    table["Score Value"]=np.round(table["Score Value"], 2)
    table["Score management"]=np.round(table["Score management"], 2)
    table["Score Dividende"]=np.round(table["Score Dividende"], 2)
    table["Final Score"]=np.round(table["Final Score"], 2)
    #table["Cours Graham"]=np.round(table["Cours Graham"], 2)
    table["Repartition"]=np.round(table["Repartition"], 2)

    return table

def TransposeTable(table, secteur):
    table2 = table[table['secteur'] == secteur]
    table2 = Update(table2)
    table2 = table2.drop(['secteur'], axis=1)
    table2 = table2.T
    table2 = table2.reindex()

    return table2

#chargement base de données
with open("picklesave",'rb') as f1:
    table=pickle.load(f1)
table=table.reset_index()
table=table.drop(['Index', 'Adresse'], axis=1)
table=scale(table)
table=table.sort_values(by=['Final Score'],ascending=False)

#General
general=table.drop(["Marge Brute","Rslt net / Dette long terme" , "Chiffre d'affaire",	"Effet Lindi", "Marque", "Scalabilité", "Brevet", "Pricing Power", "Vision long terme","Fiabilité de la direction" ,"Evolution Rslt net %",	"Evolution Benef %" , "Evolution Marge %",	"Resultat net/CA",	"Charge/CA",	"Dividende",	"Payout Ratio",	"Evolution ROE",	"ROE",	"Evolution flux tréso",	"cours",	"rendement / 5 ans"], axis=1)

class_table="table table-striped table-dark table-responsive"
class_table2="table table-striped table-dark"

app=Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

list_ticker = table['Ticker'].values.tolist()

@app.route('/', methods=['GET'])
def Home():
    return render_template('Home.html')

@app.route('/General', methods=['GET'])
def General():
    return render_template('TempTable.html', title="Classement Général", tables=[general.to_html(header=True, classes=class_table, index=False, justify="center")])

@app.route('/Secteur/Energie', methods=['GET'])
def Energie():
    energie = TransposeTable(table, 'Energie')
    return render_template('TempTable.html', tables=[energie.to_html(header=False, index=True, classes=class_table, justify="center")])

@app.route('/Secteur/Pharma', methods=['GET'])
def Pharma():
    pharma = TransposeTable(table, 'Pharma')
    return render_template('TempTable.html', tables=[pharma.to_html(header=False, index=True, classes=class_table, justify="center")])

@app.route('/Secteur/Luxe', methods=['GET'])
def Luxe():
    luxe = TransposeTable(table, 'Luxe')
    return render_template('TempTable.html', tables=[luxe.to_html(header=False, index=True, classes=class_table,justify="center")])

@app.route('/Secteur/Aeronautique', methods=['GET'])
def Aeronautique():
    aeronautique=TransposeTable(table, 'Aeronautique')
    return render_template('TempTable.html', tables=[aeronautique.to_html(header=False, index=True, classes=class_table, justify="center")])

@app.route('/Secteur/Consommation', methods=['GET'])
def Consommation():
    consommation = TransposeTable(table, 'Consommation')
    return render_template('TempTable.html', tables=[consommation.to_html(header=False, index=True, classes=class_table, justify="center")])

@app.route('/Secteur/Industrie', methods=['GET'])
def Industrie():
    industrie = TransposeTable(table, 'Industrie')
    return render_template('TempTable.html', tables=[industrie.to_html(header=False, index=True, classes=class_table, justify="center")])

@app.route('/Secteur/Logiciel', methods=['GET'])
def Logiciel():
    logiciel = TransposeTable(table, 'Logiciel')
    return render_template('TempTable.html', tables=[logiciel.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/API', methods=['GET'])
@cross_origin()
def API():
    tableJSON = Update(table)
    return tableJSON.to_json(force_ascii=False, orient="table")

@app.route('/Historic', methods=['POST'])
@cross_origin()
def Historic():
    args = request.args

    tableJSON = DATA(list_ticker)
    return args

#tableJSON.to_json(force_ascii=False, orient="table")
class HelloWorld(Resource):
    def get(self):
        raw_list = str(request.args.get("compagnie"))
        list = raw_list.split(",")
        Data = DATA(list)
        Data = Data.to_json(force_ascii=False, orient="table")
        return Data

api.add_resource(HelloWorld, '/')


#BOUCLE
if __name__ == "__main__":
    app.run(debug=True)
