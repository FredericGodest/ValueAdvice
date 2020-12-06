import pandas as pd
import yfinance as yf
import numpy as np


# import matplotlib.pyplot as plt

def DATA(Ticker_list):
    Ticker_list.append('^FCHI')
    columns = Ticker_list
    DataFrame = pd.DataFrame(columns=columns)
    for i in range(0, len(Ticker_list)):
        ticker_data = yf.Ticker(Ticker_list[i])
        data = ticker_data.history(start="2015-01-01", end="2020-11-11")["Close"]
        DataFrame[Ticker_list[i]] = data

    return DataFrame


def SIMULATEUR(Ticker_list, Weight_list, montant, start, end):
    Ticker_list.append('^FCHI')
    Ticker_list.append('^GSPC')
    Weight_list.append(1)
    Weight_list.append(1)
    data = {'Ticker': Ticker_list, 'Weight': Weight_list}
    DataFrame = pd.DataFrame(data)
    DataFrame_out = pd.DataFrame(columns=Ticker_list)

    for i in range(0, len(DataFrame)):
        ticker_data = yf.Ticker(DataFrame['Ticker'][i])
        data = ticker_data.history(start=start, end=end)["Close"]
        DataFrame_out[DataFrame['Ticker'][i]] = data * montant * DataFrame['Weight'][i] / data[0]

    for i in range(0, len(Ticker_list) - 2):
        if i == 0:
            wallet = DataFrame_out[Ticker_list[i]]
        else:
            wallet = wallet + DataFrame_out[Ticker_list[i]]

        DataFrame_out = DataFrame_out.drop(Ticker_list[i], axis=1)

    DataFrame_out["Wallet"] = wallet

    return DataFrame_out


def SIMULATEUR2(Ticker_list, Weight_list, montant, delta):
    start = "2005-11-01"
    end = "2020-11-01"
    day = 5 * 366
    data = {'Ticker': Ticker_list, 'Weight': Weight_list}
    DataFrame = pd.DataFrame(data)
    DataFrame_out = pd.DataFrame(columns=Ticker_list)

    montant = montant * delta / day

    for i in range(0, len(DataFrame)):
        ticker_data = yf.Ticker(DataFrame['Ticker'][i])
        data = ticker_data.history(start=start, end=end)["Close"]
        column = np.linspace(0, int(day / delta), int(day / delta) + 1)
        column = column.tolist()
        df = pd.DataFrame(columns=column)

        for j in range(0, int(day / delta) + 1):
            achat = (j - 1) * delta
            if achat < 0:
                achat = 1
            elif achat >= len(data):
                break

            if montant * DataFrame['Weight'][i] <= 500:
                frais = 0.99
            elif 1000 >= montant * DataFrame['Weight'][i] > 500:
                frais = 1.99
            elif 2000 >= montant * DataFrame['Weight'][i] > 1000:
                frais = 2.90
            elif 4400 >= montant * DataFrame['Weight'][i] > 2000:
                frais = 3.80
            else:
                frais = montant * DataFrame['Weight'][i] * 0.09 / 100

            df[j] = data * (montant * DataFrame['Weight'][i] - frais) / data[achat]
            df[j][0:achat - 1] = 0

        df['Total'] = df.sum(axis=1)
        DataFrame_out[DataFrame['Ticker'][i]] = df['Total'][0:len(data) - 5]

    for i in range(0, len(Ticker_list)):
        if i == 0:
            wallet = DataFrame_out[Ticker_list[i]]
        else:
            wallet = wallet + DataFrame_out[Ticker_list[i]]

        DataFrame_out = DataFrame_out.drop(Ticker_list[i], axis=1)

    DataFrame_out["Wallet"] = wallet

    return DataFrame_out

# Ticker_list = ["FP.PA","RUI.PA","SAN.PA", "BN.PA","GTT.PA","AIR.PA","OR.PA","MC.PA"]
# Weight_list = [0.18, 0.13, 0.13, 0.12, 0.19, 0.05, 0.06, 0.14]
#
# start = "2005-11-11"
# end = "2020-11-11"
#
# DAY = [7, 30, 30*2, 30*6, 365, 365*2, 365*5, 365*10]
# LABEL = ["hebdo", "mensuel", "bi-mensuel", "6 mois", "annuel", "bi-annuel", "5 ans", "one-shot"]
# RENDEMENT = []
# montant = 10000 + 300*12*15
#
# plt.subplot(211)
# for i in range(0,len(DAY)):
#     result = SIMULATEUR2(Ticker_list, Weight_list, montant, DAY[i])
#     rendement = (result["Wallet"][len(result)-1] / montant - 1) * 100
#     RENDEMENT.append(rendement)
#     plt.plot(result["Wallet"], label="Portefeuille "+ LABEL[i] + ". Rendement = " + str(np.round(rendement, 2)) + "%")
#
# plt.legend()
# plt.xlabel("Temps")
# plt.ylabel("Evolution du montant investi [Euros]")
# plt.title("Evolution du montant investi en fonction du temps et de la fréquence d'investissement")
#
#
# plt.subplot(212)
# plt.plot(DAY,RENDEMENT)
# plt.legend()
# plt.xlabel("Nombre de jour entre chaque investissement")
# plt.ylabel("Rendement esperé en %")
# plt.title("Rendement esperé comparé au nombre de jour entre chaque investissement")
# plt.show()
