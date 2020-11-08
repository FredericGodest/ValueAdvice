from wallstreet import Stock
import numpy as np

def JSON(table):
    for i in range(0, len(table)):
        cours = Stock(table.loc[i, "Ticker"]).price
        rendement_divid = np.round(table.loc[i, "Dividende"]/cours*100 , 3)

        table.loc[i, "rendement dividende"] = rendement_divid
        table.loc[i, "cours"] = cours

    tableJSON = table.to_json(force_ascii = False, orient="table")

    return tableJSON
