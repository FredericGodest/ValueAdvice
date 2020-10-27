from flask import Flask, render_template, request
import webbrowser
import os
import pandas as pd
import pickle

#chargement base de données
with open("picklesave",'rb') as f1:
    table = pickle.load(f1)
table = table.reset_index()
table = table.drop(['Index', 'Adresse'], axis=1)
table = table.sort_values(by=['Final Score'],ascending=False)



app = Flask(__name__)

@app.route('/Home', methods=['GET'])
def Home():
    return render_template('Home.html')

@app.route('/General', methods=['GET'])
def General():
    return render_template('General.html', tables=[table.to_html(header=True, index=False, classes = "table table-striped table-dark", justify="center")])


#BOUCLE
if __name__ == "__main__":
    app.run(debug=True)
