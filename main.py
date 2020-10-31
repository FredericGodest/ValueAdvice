from flask import Flask, render_template, request
import webbrowser
import os
import pandas as pd
import numpy as np
import pickle

#chargement base de données
with open("picklesave",'rb') as f1:
    table = pickle.load(f1)
table = table.reset_index()
table = table.drop(['Index', 'Adresse'], axis=1)

def scale(table):
    table["Capital"] = table["Capital"] / 1000000
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
    table["rendement / 5 ans"] = np.round(table["rendement / 5 ans"] * 100, 2)

    table["Score Value"] = np.round(table["Score Value"], 2)
    table["Score Dividende"] = np.round(table["Score Dividende"], 2)
    table["Final Score"] = np.round(table["Final Score"], 2)
    table["Cours Graham"] = np.round(table["Cours Graham"], 2)

    return table

table = scale(table)
table = table.sort_values(by=['Final Score'],ascending=False)

#General
general = table.drop(["Chiffre d'affaire",	"Evolution Rslt net %",	"Evolution Benef %" , "Evolution Marge %",	"Resultat net/CA",	"Charge/CA",	"Dividende",	"Payout Ratio",	"Evolution ROE",	"ROE",	"Evolution flux tréso",	"cours",	"rendement / 5 ans"], axis=1)

#Energie
energie = table[table['secteur']  == 'Energie']
energie = energie.drop(['secteur'], axis=1)
energie = energie.T
energie = energie.reindex()

#Pharma
pharma = table[table['secteur']  == 'Pharma']
pharma = pharma.drop(['secteur'], axis=1)
pharma = pharma.T
pharma = pharma.reindex()

#Luxe
luxe = table[table['secteur']  == 'Luxe']
luxe = luxe.drop(['secteur'], axis=1)
luxe= luxe.T
luxe = luxe.reindex()

app = Flask(__name__)

@app.route('/Home', methods=['GET'])
def Home():
    return render_template('Home.html')

@app.route('/General', methods=['GET'])
def General():
    return render_template('General.html', tables=[general.to_html(header=True, index=False, classes = "table table-striped table-dark", justify="center")])

@app.route('/Secteur/Energie', methods=['GET'])
def Energie():
    return render_template('Energie.html', tables=[energie.to_html(header=False, index=True, classes = "table table-striped table-dark", justify="center")])

@app.route('/Secteur/Pharma', methods=['GET'])
def Pharma():
    return render_template('Pharma.html', tables=[pharma.to_html(header=False, index=True, classes = "table table-striped table-dark", justify="center")])

@app.route('/Secteur/Luxe', methods=['GET'])
def Luxe():
    return render_template('Luxe.html', tables=[luxe.to_html(header=False, index=True, classes = "table table-striped table-dark", justify="center")])



#BOUCLE
if __name__ == "__main__":
    app.run(debug=True)
