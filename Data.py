from wallstreet import Stock
import numpy as np
import pandas as pd

def Update(table):
    for i in range(0, len(table)):
        #print(table.loc[i, "Ticker"])
        ticker = table["Ticker"].iloc[i]
        cours = Stock(ticker).price
        rendement_divid = np.round(table["Dividende"].iloc[i]/cours*100 , 3)
        table["rendement dividende"].iloc[i] = rendement_divid
        table["cours"].iloc[i] = cours

    return table

def UpdateTranspose(table):
    table = table.T

    for i in range(0, len(table)):
        cours = Stock(table.loc[i, "Ticker"]).price
        rendement_divid = np.round(table.loc[i, "Dividende"]/cours*100 , 3)
        table.loc[i, "rendement dividende"] = rendement_divid
        table.loc[i, "cours"] = cours

    table = table.T

    return table

