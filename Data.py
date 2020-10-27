import pandas as pd
import pickle


#chargement base de données
with open("picklesave",'rb') as f1:
    table = pickle.load(f1)
table = table.reset_index()
table = table.drop(['Index'], axis=1)
table = table.sort_values(by=['Final Score'],ascending=False)

class Classifier:

    def __init__(self,rend_divi):