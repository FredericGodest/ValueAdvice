import pandas as pd
import yfinance as yf
import numpy as np

def DATA(Ticker_list):
    Ticker_list.append('^FCHI')
    columns = Ticker_list
    DataFrame = pd.DataFrame(columns=columns)
    for i in range(0,len(Ticker_list)):
        ticker_data = yf.Ticker(Ticker_list[i])
        data = ticker_data.history(start="2015-01-01", end="2020-11-11")["Close"]
        DataFrame[Ticker_list[i]] = data

    return DataFrame

def SIMULATEUR(Ticker_list, Weight_list, montant):
    Ticker_list.append('^FCHI')
    Ticker_list.append('^GSPC')
    Weight_list.append(1)
    Weight_list.append(1)
    data = {'Ticker': Ticker_list, 'Weight': Weight_list}
    DataFrame = pd.DataFrame(data)
    DataFrame_out = pd.DataFrame(columns=Ticker_list)

    for i in range(0,len(DataFrame)):
        ticker_data = yf.Ticker(DataFrame['Ticker'][i])
        data = ticker_data.history(start="2015-01-01", end="2020-11-11")["Close"]
        DataFrame_out[DataFrame['Ticker'][i]] = data * montant * DataFrame['Weight'][i] / data[0]

    for i in range(0, len(Ticker_list)-2):
        if i == 0:
            wallet = DataFrame_out[Ticker_list[i]]
        else:
            wallet = wallet + DataFrame_out[Ticker_list[i]]

        DataFrame_out = DataFrame_out.drop(Ticker_list[i], axis=1)

    DataFrame_out["Wallet"] = wallet

    return DataFrame_out


# #Ticker_list = ["GTT.PA","OR.PA","RMS.PA"]
# Weight_list = [0.33,0.33,0.33]
#
# result = SIMULATEUR(Ticker_list, Weight_list)
#
# rendement = (result["Wallet"][len(result)-1] / 10000 - 1) * 100
# plt.plot(result["Wallet"], label="Portefeuille. Rendement = " + str(np.round(rendement, 2)) + "%")
#
# rendement = (result["^FCHI"][len(result)-1] / 10000 - 1) * 100
# plt.plot(result['^FCHI'], label = "CAC40. Rendement = " + str(np.round(rendement, 2)) + "%")
#
# rendement = (result['^GSPC'][len(result)-1] / 10000 - 1) * 100
# plt.plot(result['^GSPC'], label = "S&P500. Rendement = " + str(np.round(rendement, 2)) + "%")
# plt.legend()
# plt.show()

#print(result["^FCHI"][len(result)-1])

