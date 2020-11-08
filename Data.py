from wallstreet import Stock
import pandas as pd

def JSON(table):
    #NE PAS MODIFIER
    for i in range(0, len(table)):
        table.loc[i, "cours"] = Stock(table.loc[i, "Ticker"])

    tableJSON = table.to_json(orient="split")

    return tableJSON
