from wallstreet import Stock, Call
import pandas as pd

path_excel = r'/Users/FredericGodest/Google Drive/database2.xlsx'

#NE PAS MODIFIER
table = pd.read_excel(path_excel, sheet_name='Feuil1')
table = table.set_index(table["Index"],inplace = False)
table = table.drop(['Index'], axis=1)

#driver = webdriver.Chrome(PATH)
table = table.fillna(0)

for i in range(0,len(table)):
    print(table.loc[i, "Nom"])
    g = Stock(table.loc[i, "Ticker"])
    print(g.price)

