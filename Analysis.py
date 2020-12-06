import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import pickle

# from scipy import stats

with open("picklesave", 'rb') as f1:
    table = pickle.load(f1)

X = table["Score Value"]
Y = table["rendement dividende"] * 100

slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)


def predict(x):
    return slope * x + intercept


fitLine = predict(X)

plt.scatter(X, Y, label="données réélles")
plt.plot(X, fitLine, 'r', label="regression linéaire")
plt.xlabel("Santé financière /20")
plt.ylabel("Rendement du dividende %")
plt.title("Rendement du dividende comparé à la santé financière")
plt.legend()
plt.grid()
plt.show()
