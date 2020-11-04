from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import scipy.stats as sc
import numpy as np
import pickle


#A REMPLIR/MODIFIER
PATH = "/Applications/chromedriver" #SELENIUM PATH
#path_excel=r'/Users/FredericGodest/Desktop/Finance/database.xlsx' #EXCEL PATH
path_excel = r'/Users/FredericGodest/Google Drive/database.xlsx'

#NE PAS MODIFIER
options = Options()
options.page_load_strategy = 'normal'
table = pd.read_excel(path_excel, sheet_name='Feuil1')
table = table.set_index(table["Index"],inplace = False)
table = table.drop(['Index'], axis=1)

#driver = webdriver.Chrome(PATH)
table = table.fillna(0)

def POPUP():
    time.sleep(1)
    for _ in range(0, 100):
        try:
            button = driver.find_element_by_id("onetrust-accept-btn-handler")
            button.click()
            break
        except:
            pass

def STR2FLOAT(x, Y):
    x = x.text

    if x == '-':
        x = 0
    else:
        x = x.replace(',', '.')
        x = float(x.replace(' ', ''))

    Y.append(x)

    return x, Y

def Research(path):
    # home
    driver.get(path)
    time.sleep(1)
    Capital = driver.find_element_by_xpath("/html/body/div[5]/section/div[9]/div[8]/span[2]")
    Capital = Capital.text
    Capital = Capital.replace(',', '')
    Capital = Capital.replace('B', '0000000')
    Capital = float(Capital.replace('M', '0000'))

    # Income Statement
    path1 = path
    path = path1 + "-income-statement"
    driver.get(path)

    Year = [2019, 2018, 2017, 2016]
    CA = []
    RESULT_NET = []
    CHARGE = []
    BPA = []
    DIVID = []
    BENEF = []

    # cliquer sur annuel
    button = driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/div[1]/a[1]")
    button.click()
    time.sleep(1)

    for i in range(0, 4):
        rank = str(i + 2)

        while True:
            try:
                ca = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[1]/td[" + str(rank) + "]")
                result_net = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[13]/td[" + str(rank) + "]")
                charge = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[5]/td[" + str(rank) + "]")
                divid = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[26]/td[" + str(rank) + "]")
                bpa = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[27]/td[" + str(rank) + "]")
                benef = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[4]/td[" + str(rank) + "]")
                break
            except:
                pass

        ca, CA = STR2FLOAT(ca, CA)
        result_net, RESULT_NET = STR2FLOAT(result_net, RESULT_NET)
        charge, CHARGE = STR2FLOAT(charge, CHARGE)
        bpa, BPA = STR2FLOAT(bpa, BPA)
        divid, DIVID = STR2FLOAT(divid, DIVID)
        benef, BENEF = STR2FLOAT(benef, BENEF)

    # balance-sheet
    path = path1 + "-balance-sheet"
    driver.get(path)

    CAPITAUX_PROPRE = []

    # cliquer sur annuel
    button = driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/div[1]/a[1]")
    button.click()
    time.sleep(1)

    for i in range(0, 4):
        rank = str(i + 2)

        while True:
            try:
                capitaux_propre = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[9]/td[" + str(rank) + "]")
                break
            except:
                pass

        capitaux_propre, CAPITAUX_PROPRE = STR2FLOAT(capitaux_propre, CAPITAUX_PROPRE)

    # balance-sheet
    path = path1 + "-cash-flow"
    driver.get(path)

    CASH_FLOW = []

    # cliquer sur annuel
    button = driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/div[1]/a[1]")
    button.click()
    time.sleep(1)

    for i in range(0, 4):
        rank = str(i + 2)

        while True:
            try:
                cashflow = driver.find_element_by_xpath(
                    "/html/body/div[5]/section/div[9]/table/tbody[2]/tr[12]/td[" + str(rank) + "]")
                break
            except:
                pass

        cashflow, CASH_FLOW = STR2FLOAT(cashflow, CASH_FLOW)

    # Chiffre d'affaire
    droite = sc.linregress(Year, CA)
    prog_CA = droite.slope / np.mean(CA)
    Chiffre_Affaire = np.mean(CA)

    # Resultat NET
    droite = sc.linregress(Year, RESULT_NET)
    prog_RN = droite.slope / np.mean(RESULT_NET)
    Resultat_net = np.mean(RESULT_NET)

    # Charge d'exploitation
    Charge = np.mean(CHARGE)

    # Dividende
    droite = sc.linregress(Year, DIVID)
    prog_divid = droite.slope / np.mean(DIVID)
    Divid = DIVID[3]

    # BPA
    droite = sc.linregress(Year, BPA)
    prog_BPA = droite.slope / np.mean(BPA)
    BPA = BPA[3]

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

    # CASH_FLOW
    droite = sc.linregress(Year, CASH_FLOW)
    prog_CASH = droite.slope / np.mean(CASH_FLOW)

    # cours
    cours = driver.find_element_by_xpath("/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]")
    cours = cours.text
    cours = cours.replace(',', '.')
    cours = float(cours.replace(' ', ''))

    # Rendement action 5 ans
    path = path1 + "-ratios"
    driver.get(path)
    rendement = driver.find_element_by_xpath(
        "/html/body/div[5]/section/table/tbody/tr[16]/td/div/table/tbody/tr[2]/td[2]")
    rendement = rendement.text
    if rendement == '-':
        rendement = 0
    else:
        rendement = rendement.replace(',', '.')
        rendement = rendement.replace('%', '')
        rendement = float(rendement.replace(' ', ''))
        rendement = rendement / 100

    BVPS = driver.find_element_by_xpath("/html/body/div[5]/section/table/tbody/tr[6]/td/div/table/tbody/tr[4]/td[2]")
    BVPS = BVPS.text
    BVPS = BVPS.replace(',', '.')
    BVPS = float(BVPS.replace(' ', ''))

    Graham = np.sqrt(20 / 1.5 * BPA * BVPS)

    return Chiffre_Affaire, prog_CA, Resultat_net, prog_RN, Charge, prog_BPA, BPA, Divid, prog_divid, Marge_brut, prog_MB, prog_Benef, prog_ROE, ROE, prog_CASH, cours, rendement, Capital, Graham

def Scoring(j):
    point = 0
    rank = 0

    # price
    rank += 1
    if table.loc[j, "Cours Graham"] >= table.loc[j, "cours"]:
        point += 1

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
    rank += 1
    if table.loc[j, "Capital"] >= 2000000000:
        point += 1

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


a = input("Souhaites-tu tout mettre à jour ? (Y/N)")
driver = webdriver.Chrome(PATH)

for j in range(0, len(table)):
    print(table.loc[j, "Nom"])
    path = table.loc[j, "Adresse"]

    if a == "N":
        if path != "" and table.loc[j, "Chiffre d'affaire"] == 0:
            POPUP()

            Chiffre_Affaire, prog_CA, Resultat_net, prog_RN, Charge, prog_BPA, BPA, Divid, prog_divid, Marge_brut, prog_MB, prog_Benef, prog_ROE, ROE, prog_CASH, cours, rendement, Capital, Graham = Research(
                path)

            table.loc[j, "Cours Graham"] = Graham
            table.loc[j, "Chiffre d'affaire"] = Chiffre_Affaire
            table.loc[j, "Evolution CA %"] = prog_CA

            table.loc[j, "Capital"] = Capital
            table.loc[j, "Evolution Rslt net %"] = prog_RN
            table.loc[j, "Resultat net/CA"] = Resultat_net / Chiffre_Affaire

            table.loc[j, "Charge/CA"] = Charge / Chiffre_Affaire

            table.loc[j, "Evolution BPA %"] = prog_BPA
            table.loc[j, "Evolution Dividende %"] = prog_divid
            table.loc[j, "Dividende"] = Divid
            table.loc[j, "Payout Ratio"] = Divid / BPA

            table.loc[j, "Evolution Benef %"] = prog_Benef
            table.loc[j, "Marge Brute"] = Marge_brut
            table.loc[j, "Evolution Marge %"] = prog_MB

            table.loc[j, "Evolution ROE"] = prog_ROE
            table.loc[j, "ROE"] = ROE

            table.loc[j, "Evolution flux tréso"] = prog_CASH

            table.loc[j, "cours"] = cours
            table.loc[j, "rendement / 5 ans"] = rendement

            table.loc[j, "rendement dividende"] = Divid / cours

            # sauvegarde
            table.to_excel(path_excel, sheet_name='Feuil1')

    elif a == "Y":
        if path != "":
            POPUP()

            Chiffre_Affaire, prog_CA, Resultat_net, prog_RN, Charge, prog_BPA, BPA, Divid, prog_divid, Marge_brut, prog_MB, prog_Benef, prog_ROE, ROE, prog_CASH, cours, rendement, Capital, Graham = Research(
                path)

            table.loc[j, "Cours Graham"] = Graham
            table.loc[j, "Chiffre d'affaire"] = Chiffre_Affaire
            table.loc[j, "Evolution CA %"] = prog_CA

            table.loc[j, "Capital"] = Capital
            table.loc[j, "Evolution Rslt net %"] = prog_RN
            table.loc[j, "Resultat net/CA"] = Resultat_net / Chiffre_Affaire

            table.loc[j, "Charge/CA"] = Charge / Chiffre_Affaire

            table.loc[j, "Evolution BPA %"] = prog_BPA
            table.loc[j, "Evolution Dividende %"] = prog_divid
            table.loc[j, "Dividende"] = Divid
            table.loc[j, "Payout Ratio"] = Divid / BPA

            table.loc[j, "Evolution Benef %"] = prog_Benef
            table.loc[j, "Marge Brute"] = Marge_brut
            table.loc[j, "Evolution Marge %"] = prog_MB

            table.loc[j, "Evolution ROE"] = prog_ROE
            table.loc[j, "ROE"] = ROE

            table.loc[j, "Evolution flux tréso"] = prog_CASH

            table.loc[j, "cours"] = cours
            table.loc[j, "rendement / 5 ans"] = rendement

            table.loc[j, "rendement dividende"] = Divid / cours

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
    table.to_excel(r'/Users/FredericGodest/Google Drive/database.xlsx', sheet_name='Feuil1')
    table.to_excel(r'/Users/FredericGodest/Desktop/Finance/database.xlsx', sheet_name='Feuil1')  # EXCEL PATH

driver.quit()

# Save Pickle
with open(r"/Users/FredericGodest/PycharmProjects/yahou invest/picklesave", 'wb') as f1:
    pickle.dump(table, f1)