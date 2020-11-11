import pandas as pd
import yfinance as yf

def DATA(Ticker_list):
    Ticker_list.append('^FCHI')
    columns = Ticker_list
    DataFrame = pd.DataFrame(columns=columns)
    for i in range(0,len(Ticker_list)):
        ticker_data = yf.Ticker(Ticker_list[i])
        data = ticker_data.history(start="2015-01-01", end="2020-11-11")["Close"]
        DataFrame[Ticker_list[i]] = data

    return DataFrame

