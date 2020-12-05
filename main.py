import pickle
import numpy as np
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from Data import Update
from Historic import DATA, SIMULATEUR
from flask_restful import Resource, request, Api


# Fonction Perso
def scale(table):
    # table["Capital"]=table["Capital"] / 1000000
    table["Evolution CA %"] = np.round(table["Evolution CA %"] * 100, 2)
    table["Evolution Rslt net %"] = np.round(table["Evolution Rslt net %"] * 100, 2)
    table["Evolution Benef %"] = np.round(table["Evolution Benef %"] * 100, 2)
    table["Marge Brute"] = np.round(table["Marge Brute"] * 100, 2)
    table["Evolution Marge %"] = np.round(table["Evolution Marge %"] * 100, 2)
    table["Resultat net/CA"] = np.round(table["Resultat net/CA"] * 100, 2)
    table["Charge/CA"] = np.round(table["Charge/CA"] * 100, 2)
    table["Evolution BPA %"] = np.round(table["Evolution BPA %"] * 100, 2)
    table["Evolution Dividende %"] = np.round(table["Evolution Dividende %"] * 100, 2)
    table["rendement dividende"] = np.round(table["rendement dividende"] * 100, 2)
    table["Payout Ratio"] = np.round(table["Payout Ratio"] * 100, 2)
    table["Evolution ROE"] = np.round(table["Evolution ROE"] * 100, 2)
    table["ROE"] = np.round(table["ROE"] * 100, 2)
    table["Evolution flux tréso"] = np.round(table["Evolution flux tréso"] * 100, 2)
    table["rendement / 5 ans"] = np.round(table["rendement / 5 ans"], 2)

    table["Score Value"] = np.round(table["Score Value"], 2)
    table["Score management"] = np.round(table["Score management"], 2)
    table["Score Dividende"] = np.round(table["Score Dividende"], 2)
    table["Final Score"] = np.round(table["Final Score"], 2)
    table["Prix Juste (Futur)"] = np.round(table["Prix Juste (Futur)"], 2)
    table["Repartition"] = np.round(table["Repartition"], 2)

    return table


def TransposeTable(table, secteur):
    _table = table[table['secteur'] == secteur]
    _table = Update(_table)
    _table = _table.drop(['secteur'], axis=1)
    _table = _table.T
    _table = _table.reindex()

    return _table


# chargement base de données
with open("picklesave", 'rb') as f1:
    table = pickle.load(f1)
table = table.reset_index()
table = table.drop(['Index', 'Adresse'], axis=1)
table = scale(table)
table = table.sort_values(by=['Final Score'], ascending=False)

# General
# general=table.drop(["Marge Brute","Dette long terme / Rslt net" , "Chiffre d'affaire",	"Effet Lindi", "Marque", "Scalabilité", "Brevet", "Pricing Power", "Vision long terme","Fiabilité de la direction" ,"Evolution Rslt net %",	"Evolution Benef %" , "Evolution Marge %",	"Resultat net/CA",	"Charge/CA",	"Dividende",	"Payout Ratio",	"Evolution ROE",	"ROE",	"Evolution flux tréso",	"cours",	"rendement / 5 ans"], axis=1)
general = table[["Nom", "secteur", "cours", "Prix Juste (Futur)", "Score Value", "Score Dividende", "Score management",
                 "Final Score", "Repartition", "Eligibilité"]]
energie = TransposeTable(table, 'Energie')
pharma = TransposeTable(table, 'Pharma')
luxe = TransposeTable(table, 'Luxe')
aeronautique = TransposeTable(table, 'Aeronautique')
consommation = TransposeTable(table, 'Consommation')
industrie = TransposeTable(table, 'Industrie')
logiciel = TransposeTable(table, 'Logiciel')

class_table = "table card-table table-vcenter text-nowrap table-striped datatable"

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def Home():
    return render_template('pages/Home.html')


@app.route('/General', methods=['GET'])
def General():
    return render_template('pages/TempTable.html', title="Classement Général", tables=[general.to_html(header=True, classes=class_table, index=False, justify="center")])


@app.route('/Secteur/Energie', methods=['GET'])
def Energie():
    return render_template('pages/TempTable.html', title="Energie", tables=[energie.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Pharma', methods=['GET'])
def Pharma():
    return render_template('pages/TempTable.html', title="Pharmaceutique", tables=[pharma.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Luxe', methods=['GET'])
def Luxe():
    return render_template('pages/TempTable.html', title="Luxe", tables=[luxe.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Aeronautique', methods=['GET'])
def Aeronautique():
    return render_template('pages/TempTable.html', title="Aeronautique", tables=[aeronautique.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Consommation', methods=['GET'])
def Consommation():
    return render_template('pages/TempTable.html', title="Consommation", tables=[consommation.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Industrie', methods=['GET'])
def Industrie():
    return render_template('pages/TempTable.html', title="Industrie", tables=[industrie.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Secteur/Logiciel', methods=['GET'])
def Logiciel():
    return render_template('pages/TempTable.html', title="Logiciel", tables=[logiciel.to_html(header=False, index=True, classes=class_table, justify="center")])


@app.route('/Simulateur', methods=['GET'])
def Simulateur():
    return render_template('pages/Simulateur.html')


@app.route('/Documentation', methods=['GET'])
def Documentation():
    return render_template('pages/Documentation.html')


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found():
    return render_template('pages/404.html'), 404


@app.route('/API', methods=['GET'])
@cross_origin()
def API():
    tableJSON = Update(table)
    return tableJSON.to_json(force_ascii=False, orient="table")


class DATA_Histo(Resource):
    @staticmethod
    def get():
        raw_list = str(request.args.get("compagnie"))
        list = raw_list.split(",")
        Data = DATA(list)
        Data = Data.to_json(force_ascii=False, orient="table")
        return Data


api.add_resource(DATA_Histo, '/DATA')


class SIMUL(Resource):
    @staticmethod
    def get():
        raw_list = str(request.args.get("compagny"))
        Ticker_list = raw_list.split(",")
        raw_list = str(request.args.get("weight"))
        Weight_list = raw_list.split(",")
        montant = float(request.args.get("amount"))
        start = str(request.args.get("start"))
        end = str(request.args.get("end"))

        new_Weight_list = []
        i = 0
        for item in Weight_list:
            new_Weight_list.append(float(item))
            new_Weight_list[i] = new_Weight_list[i] / 100
            i += 1

        Data = SIMULATEUR(Ticker_list, new_Weight_list, montant, start, end)
        Data = Data.to_json(force_ascii=False, orient="table")
        return Data


api.add_resource(SIMUL, '/SIMULATEUR')

# /SIMULATEUR?compagny=GTT.PA,OR.PA&weight=50,50&amount=10000&start=2014-11-11&end=2020-11-11

# BOUCLE
if __name__ == "__main__":
    app.run(debug=True)
