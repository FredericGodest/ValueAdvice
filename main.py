from flask import Flask, render_template, request
import webbrowser
import os
import pandas as pd
import numpy as np
import pickle

#Fonction Perso
def scale(table):
    table["Capital"]=table["Capital"] / 1000000
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
    table["rendement / 5 ans"]=np.round(table["rendement / 5 ans"] * 100, 2)

    table["Score Value"]=np.round(table["Score Value"], 2)
    table["Score management"]=np.round(table["Score management"], 2)
    table["Score Dividende"]=np.round(table["Score Dividende"], 2)
    table["Final Score"]=np.round(table["Final Score"], 2)
    table["Cours Graham"]=np.round(table["Cours Graham"], 2)
    table["Repartition"]=np.round(table["Repartition"], 2)

    return table

def TransposeTable(table, secteur):
    table2=table[table['secteur'] == secteur]
    table2=table2.drop(['secteur'], axis=1)
    table2=table2.T
    table2=table2.reindex()

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

#Aeronautique
aeronautique=TransposeTable(table, 'Aeronautique')

#Consommation
consommation=TransposeTable(table, 'Consommation')

#Energie
energie=TransposeTable(table, 'Energie')

#Industrie
industrie=TransposeTable(table, 'Industrie')

#Logiciel
logiciel=TransposeTable(table, 'Logiciel')

#Pharma
pharma=TransposeTable(table, 'Pharma')

#Luxe
luxe=TransposeTable(table, 'Luxe')

class_table="table table-striped table-dark table-responsive"
class_table2="table table-striped table-dark"

app=Flask(__name__)

@app.route('/', methods=['GET'])
def Home():
    return render_template('Home.html')

@app.route('/General', methods=['GET'])
def General():
    return render_template('TempTable.html', title="Classement Général", tables=[general.to_html(header=True, classes=class_table, index=False, justify="center")])

@app.route('/Secteur/Energie', methods=['GET'])
def Energie():
    return render_template('TempTable.html', tables=[energie.to_html(header=False, index=True, classes=class_table2, justify="center")])

@app.route('/Secteur/Pharma', methods=['GET'])
def Pharma():
    return render_template('TempTable.html', tables=[pharma.to_html(header=False, index=True, classes=class_table2, justify="center")])

@app.route('/Secteur/Luxe', methods=['GET'])
def Luxe():
    return render_template('TempTable.html', tables=[luxe.to_html(header=False, index=True, classes=class_table2,justify="center")])

@app.route('/Secteur/Aeronautique', methods=['GET'])
def Aeronautique():
    return render_template('TempTable.html', tables=[aeronautique.to_html(header=False, index=True, classes=class_table2, justify="center")])

@app.route('/Secteur/Consommation', methods=['GET'])
def Consommation():
    return render_template('TempTable.html', tables=[consommation.to_html(header=False, index=True, classes=class_table2, justify="center")])

@app.route('/Secteur/Industrie', methods=['GET'])
def Industrie():
    return render_template('TempTable.html', tables=[industrie.to_html(header=False, index=True, classes=class_table2, justify="center")])

@app.route('/Secteur/Logiciel', methods=['GET'])
def Logiciel():
    return render_template('TempTable.html', tables=[logiciel.to_html(header=False, index=True, classes=class_table2, justify="center")])


#BOUCLE
if __name__ == "__main__":
    app.run(debug=True)
