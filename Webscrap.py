from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import scipy.stats as sc
import numpy as np
import pickle
from wallstreet import Stock


#A REMPLIR/MODIFIER
PATH = "/Applications/chromedriver" #SELENIUM PATH
#path_excel=r'/Users/FredericGodest/Desktop/Finance/database.xlsx' #EXCEL PATH
path_excel = r'/Users/FredericGodest/Google Drive/database2.xlsx'

#NE PAS MODIFIER
options = Options()
options.page_load_strategy = 'normal'
table = pd.read_excel(path_excel, sheet_name='Feuil1')
table = table.set_index(table["Index"],inplace = False)
table = table.drop(['Index'], axis=1)

#driver = webdriver.Chrome(PATH)
table = table.fillna(0)

def STR2FLOAT(x, Y):
    x = x.text

    if x == '-':
        x = 0
    else:
        x = x.replace(',', '.')
        x = float(x.replace(' ', ''))

    Y.append(x)

    return x, Y

def Research(path,ticker):
    #COMPTE DE RESULTAT
    driver.get(path)
    time.sleep(1)

    Year = [2015, 2016, 2017, 2018, 2019]
    CA = []
    RESULT_NET = []
    CHARGE = []
    BPA = []
    BENEF = []

    for i in range(0, 5):
        rank = str(i + 1)
        while True:
            try:
                ca = driver.find_element_by_xpath("/ html / body / div[2] / div[2] / form / div[4] / div[2] / div / div / div[3] / div[2] / table / tbody[1] / tr[1] / td[" + str(rank) + "]")
                result_net = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[3]/tr[5]/td[" + str(rank) + "]")
                charge = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[7]/td[" + str(rank) + "]")
                bpa = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[5]/tr[3]/td[" + str(rank) + "]")
                benef = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[4]/tr/td[" + str(rank) + "]")
                break
            except:
                print("erreur de chargement de données pour Resultat")
                pass

        ca, CA = STR2FLOAT(ca, CA)
        result_net, RESULT_NET = STR2FLOAT(result_net, RESULT_NET)
        charge, CHARGE = STR2FLOAT(charge, CHARGE)
        bpa, BPA = STR2FLOAT(bpa, BPA)
        benef, BENEF = STR2FLOAT(benef, BENEF)

    #BILAN COMPTABLE
    # cliquer sur Bilan
    button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[2]/ul[3]/li[2]/a")
    button.click()
    time.sleep(1)

    CAPITAUX_PROPRE = []
    DETTE_LONG = []
    TRESO = []

    for i in range(0, 5):
        rank = str(i + 1)
        while True:
            try:
                capitaux_propre = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[21]/td[" + str(rank) + "]")
                dette_long = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[11]/td["+ str(rank) +"]")
                treso = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[1]/tr[4]/td["+ str(rank) +"]")
                break
            except:
                print("erreur de chargement de données pour Bilan")
                pass

        capitaux_propre, CAPITAUX_PROPRE = STR2FLOAT(capitaux_propre, CAPITAUX_PROPRE)
        dette_long, DETTE_LONG = STR2FLOAT(dette_long, DETTE_LONG)
        treso, TRESO = STR2FLOAT(treso, TRESO)

    #DIVIDENDE
    # cliquer sur Bilan
    button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[2]/ul[3]/li[4]/a")
    button.click()
    time.sleep(1)
    DIVID = []

    for i in range(0, 10):
        rank = str(i + 1)
        while True:
            try:
                dividende = driver.find_element_by_xpath('// *[ @ id = "HistoricalDividends"] / table / tbody / tr['+ str(rank) +'] / td[6]')
                break
            except:
                print("erreur de chargement de données pour Dividende")
                pass

        dividende, DIVID = STR2FLOAT(dividende, DIVID)

    #Performance
    # cliquer sur Cours
    button = driver.find_element_by_xpath("/ html / body / div[2] / div[2] / form / div[4] / div[2] / div / div / div[2] / ul[2] / li[1] / a")
    button.click()
    time.sleep(2)

    while True:
        try:
            capital = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div/div[1]/table/tbody/tr/td[5]')
            capital = capital.text
            break
        except:
            pass

    # cliquer sur Performance
    button = driver.find_element_by_xpath("/ html / body / div[2] / div[2] / form / div[4] / div[2] / div / div / div[2] / ul[3] / li[3] / a")
    button.click()
    time.sleep(2)

    while True:
        try:
            rendement = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[3]/table/tbody/tr/td[5]')
            break
        except:
            pass

    #rendement
    rendement = rendement.text
    rendement = float(rendement.replace(',', '.'))

    # Chiffre d'affaire
    droite = sc.linregress(Year, CA)
    prog_CA = droite.slope / np.mean(CA)
    Chiffre_Affaire = np.mean(CA)

    # Resultat NET
    droite = sc.linregress(Year, RESULT_NET)
    prog_RN = droite.slope / np.mean(RESULT_NET)
    rslt_net = np.mean(RESULT_NET)
    rslt_CA = rslt_net/Chiffre_Affaire

    # Charge d'exploitation
    Charge = np.mean(CHARGE)
    Charge = Charge/Chiffre_Affaire

    # BPA
    droite = sc.linregress(Year, BPA)
    prog_BPA = droite.slope / np.mean(BPA)
    BPA = BPA[4]

    # MARGE
    BENEF = np.asarray(BENEF)
    CA = np.asarray(CA)
    Marge_brut = BENEF / CA
    droite = sc.linregress(Year, Marge_brut)
    prog_MB = droite.slope / np.mean(Marge_brut)
    Marge_brut = np.mean(Marge_brut)

    # Benef
    droite = sc.linregress(Year, BENEF)
    prog_Benef = droite.slope / np.mean(BENEF)

    # ROE
    CAPITAUX_PROPRE = np.asarray(CAPITAUX_PROPRE)
    RESULT_NET = np.asarray(RESULT_NET)
    ROE = RESULT_NET / CAPITAUX_PROPRE
    droite = sc.linregress(Year, ROE)
    prog_ROE = droite.slope / np.mean(ROE)
    ROE = np.mean(ROE)

    #Dette long terme
    Rslt_DetteLong = rslt_net/np.mean(DETTE_LONG)

    # TRESO
    droite = sc.linregress(Year, TRESO)
    prog_treso = droite.slope / np.mean(TRESO)

    # Dividende
    Year_divid = np.linspace(9,0,10)
    droite = sc.linregress(Year_divid, DIVID)
    prog_divid = droite.slope / np.mean(DIVID)
    Divid = DIVID[0]

    #Cours
    s = Stock(ticker)
    cours = s.price

    table_out = {"Capital" : [capital],
    "Chiffre d'affaire" : [Chiffre_Affaire],
    "Evolution CA %" : [prog_CA],
    "Evolution Rslt net %" :[prog_RN],
    "Evolution Benef %" : [prog_Benef],
    "Marge Brute" : [Marge_brut],
    "Evolution Marge %" : [prog_MB],
    "Resultat net / CA" : [rslt_CA],
    "Rslt net / Dette long terme" : [Rslt_DetteLong],
    "Charge / CA" : [Charge],
    "Evolution BPA %" : [prog_BPA],
    "Evolution Dividende %" : [prog_divid],
    "Dividende" : [Divid],
    "rendement dividende" : [Divid/cours],
    "Payout Ratio" : [Divid / BPA],
    "Evolution ROE" : [prog_ROE],
    "ROE" : [ROE],
    "Evolution flux tréso" : [prog_treso],
    "cours" : [cours],
    "Cours Graham" : [],
    "rendement / 5 ans" : [rendement]}

    return table_out

def Scoring(j):
    point = 0
    rank = 0

    # price
    #rank += 1
    #if table.loc[j, "Cours Graham"] >= table.loc[j, "cours"]:
        #point += 1

    # Chiffre d'affaire
    rank += 1
    if table.loc[j, "Evolution CA %"] >= 0:
        point += 1

    # resultat Net
    rank += 1
    if table.loc[j, "Evolution Rslt net %"] >= 0:
        point += 1

    # benefice
    rank += 1
    if table.loc[j, "Evolution Benef %"] >= 0:
        point += 1

    # Marge Brute
    rank += 1
    if table.loc[j, "Marge Brute"] >= 0.4:
        point += 1

    # Evolution Marge
    rank += 1
    if table.loc[j, "Evolution Marge %"] >= -5 / 100:
        point += 1

    # Resultat net/CA
    rank += 1
    if table.loc[j, "Resultat net/CA"] >= 0.2:
        point += 1

    # Charge/CA
    rank += 1
    if table.loc[j, "Charge/CA"] <= 0.2:
        point += 1

    # Evolution BPA
    rank += 1
    if table.loc[j, "Evolution BPA %"] >= 0:
        point += 1

    # Payout Ratio
    rank += 1
    if table.loc[j, "Payout Ratio"] <= 0.65:
        point += 1

        # Evolution ROE
    rank += 1
    if table.loc[j, "Evolution ROE"] >= -0.02:
        point += 1

        # ROE
    rank += 1
    if table.loc[j, "ROE"] >= 0.2:
        point += 1

        # Evolution Cash Flow
    rank += 1
    if table.loc[j, "Evolution flux tréso"] >= 0.05:
        point += 1

        # rendement
    rank += 1
    if table.loc[j, "rendement / 5 ans"] >= 0.015:
        point += 1

    score = point / rank * 20

    return score

def Score_Dividende(j):
    point = 0
    rank = 0

    # Capitalisation
    #rank += 1
    #if table.loc[j, "Capital"] >= 2000000000:
     #   point += 1

        # CA
    rank += 1
    if table.loc[j, "Chiffre d'affaire"] <= 10000:
        point += 1

    # Evolution CA
    rank += 1
    if table.loc[j, "Evolution CA %"] >= 0:
        point += 1

    # Evolution Dividende
    rank += 1
    if table.loc[j, "Evolution Dividende %"] >= 0:
        point += 1

    # Rendement dividende
    rank += 1
    if table.loc[j, "rendement dividende"] >= 0.03 and table.loc[j, "rendement dividende"] < 0.085:
        point += 1

    # Payout Ratio
    rank += 1
    if table.loc[j, "Payout Ratio"] <= 0.7:
        point += 1

        # rendement
    rank += 1
    if table.loc[j, "rendement / 5 ans"] >= 0.015:
        point += 1

    score = point / rank * 20

    return score

def LoadingData(table,table_out):
    table.loc[j, "Cours Graham"] = "pas encore évalué"
    table.loc[j, "Chiffre d'affaire"] = table_out["Chiffre d'affaire"]
    table.loc[j, "Evolution CA %"] = table_out["Evolution CA %"]

    table.loc[j, "Capital"] = table_out["Capital"]
    table.loc[j, "Evolution Rslt net %"] = table_out["Evolution Rslt net %"]
    table.loc[j, "Resultat net/CA"] = table_out["Resultat net / CA"]

    table.loc[j, "Charge/CA"] = table_out["Charge / CA"]

    table.loc[j, "Evolution BPA %"] = table_out["Evolution BPA %"]
    table.loc[j, "Evolution Dividende %"] = table_out["Evolution Dividende %"]
    table.loc[j, "Dividende"] = table_out["Dividende"]
    table.loc[j, "Payout Ratio"] = table_out["Payout Ratio"]

    table.loc[j, "Evolution Benef %"] = table_out["Evolution Benef %"]
    table.loc[j, "Marge Brute"] = table_out["Marge Brute"]
    table.loc[j, "Evolution Marge %"] = table_out["Evolution Marge %"]

    table.loc[j, "Evolution ROE"] = table_out["Evolution ROE"]
    table.loc[j, "ROE"] = table_out["ROE"]

    table.loc[j, "Evolution flux tréso"] = table_out["Evolution flux tréso"]

    table.loc[j, "cours"] = table_out["cours"]
    table.loc[j, "rendement / 5 ans"] = table_out["rendement / 5 ans"]

    table.loc[j, "rendement dividende"] = table_out["rendement dividende"]

    table.loc[j, "Rslt net / Dette long terme"] = table_out["Rslt net / Dette long terme"]

    return table


a = input("Souhaites-tu tout mettre à jour ? (Y/N)")

driver = webdriver.Chrome(PATH)

for j in range(0, 2):  #len(table)
    print(table.loc[j, "Nom"])
    path = table.loc[j, "Adresse"]

    if a == "N":
        if path != "" and table.loc[j, "Chiffre d'affaire"] == 0:
            ticker = table.loc[j,'Ticker']
            table_out = Research(path,ticker)
            table = LoadingData(table,table_out)

            # sauvegarde
            table.to_excel(path_excel, sheet_name='Feuil1')

    elif a == "Y":
        if path != "":
            ticker = table.loc[j, 'Ticker']
            table_out = Research(path, ticker)
            table = LoadingData(table, table_out)

            # sauvegarde
            table.to_excel(path_excel, sheet_name='Feuil1')

    # Etape de scoring
    score = Scoring(j)
    table.loc[j, "Score Value"] = score

    score2 = Score_Dividende(j)
    table.loc[j, "Score Dividende"] = score2

    score_final = (score * 2 + score2) / 3
    table.loc[j, "Final Score"] = score_final

    Repartition = (score_final / 20 * 2 - 1) * 100 / 2
    if Repartition <= 0:
        Repartition = 0
    table.loc[j, "Repartition"] = Repartition

    table.to_excel(path_excel, sheet_name='Feuil1')
    table.to_excel(r'/Users/FredericGodest/Google Drive/database2.xlsx', sheet_name='Feuil1')
    #table.to_excel(r'/Users/FredericGodest/Desktop/Finance/database.xlsx', sheet_name='Feuil1')  # EXCEL PATH

driver.quit()

# Save Pickle
with open(r"/Users/FredericGodest/PycharmProjects/yahou invest/picklesave", 'wb') as f1:
    pickle.dump(table, f1)