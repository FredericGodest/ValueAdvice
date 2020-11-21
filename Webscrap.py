from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
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
options.page_load_strategy = 'eager'
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
    EBITDA = []

    for i in range(0, 5):
        rank = str(i + 1)
        while True:
            try:
                ca = driver.find_element_by_xpath("/ html / body / div[2] / div[2] / form / div[4] / div[2] / div / div / div[3] / div[2] / table / tbody[1] / tr[1] / td[" + str(rank) + "]")
                result_net = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[3]/tr[5]/td[" + str(rank) + "]")
                charge = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[7]/td[" + str(rank) + "]")
                bpa = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[5]/tr[3]/td[" + str(rank) + "]")
                benef = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[4]/tr/td[" + str(rank) + "]")
                ebitda = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[8]/td[" + str(rank) + "]")
                break
            except:
                print("erreur de chargement de données pour Resultat")
                pass

        ca, CA = STR2FLOAT(ca, CA)
        result_net, RESULT_NET = STR2FLOAT(result_net, RESULT_NET)
        charge, CHARGE = STR2FLOAT(charge, CHARGE)
        bpa, BPA = STR2FLOAT(bpa, BPA)
        benef, BENEF = STR2FLOAT(benef, BENEF)
        ebitda, EBITDA = STR2FLOAT(ebitda, EBITDA)

    #BILAN COMPTABLE
    # cliquer sur Bilan
    button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[2]/ul[3]/li[2]/a")
    button.click()
    time.sleep(1)

    CAPITAUX_PROPRE = []
    DETTE_LONG = []
    TRESO = []
    TOT_ACTIF = []
    DETTE_COURANTE = []
    DETTE_FOURNISSEUR = []

    for i in range(0, 5):
        rank = str(i + 1)
        while True:
            try:
                tot_actif = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[1]/tr[18]/td[" + str(rank) + "]")
                capitaux_propre = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[21]/td[" + str(rank) + "]")
                dette_long = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[11]/td["+ str(rank) +"]")
                treso = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[1]/tr[4]/td["+ str(rank) +"]")

                dette_fournisseur = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[4]/td["+ str(rank) +"]")
                dette_courante = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[3]/div[2]/table/tbody[2]/tr[6]/td["+ str(rank) +"]")
                break
            except:
                print("erreur de chargement de données pour Bilan")
                pass

        tot_actif, TOT_ACTIF = STR2FLOAT(tot_actif, TOT_ACTIF)
        capitaux_propre, CAPITAUX_PROPRE = STR2FLOAT(capitaux_propre, CAPITAUX_PROPRE)
        dette_long, DETTE_LONG = STR2FLOAT(dette_long, DETTE_LONG)
        treso, TRESO = STR2FLOAT(treso, TRESO)

        dette_fournisseur, DETTE_FOURNISSEUR = STR2FLOAT(dette_fournisseur, DETTE_FOURNISSEUR)
        dette_courante, DETTE_COURANTE = STR2FLOAT(dette_courante, DETTE_COURANTE)


    #DIVIDENDE
    # cliquer sur Bilan
    button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div[4]/div[2]/div/div/div[2]/ul[3]/li[4]/a")
    button.click()
    time.sleep(2)
    DIVID = []
    C = 0
    k = 0

    for i in range(0, 10):
        rank = str(i + 1)
        while True:
            try:
                dividende = driver.find_element_by_xpath('// *[ @ id = "HistoricalDividends"] / table / tbody / tr['+ str(rank) +'] / td[6]')
                break

            except:
                if len(DIVID)>=1:
                    C = 1
                    break
                else:
                    print("erreur de chargement de données pour Dividende")
                    time.sleep(1)
                    k += 1
                    if k >=4:
                        C=1
                        dividende = 0
                        break
                    else:
                        pass

        if C == 0:
            dividende, DIVID = STR2FLOAT(dividende, DIVID)
        else :
            DIVID = [0]
            break

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
    if rendement == '-':
        rendement = 0
    else :
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
    Rslt_DetteLong = np.mean(DETTE_LONG)/rslt_net

    # TRESO
    droite = sc.linregress(Year, TRESO)
    prog_treso = droite.slope / np.mean(TRESO)

    # Dividende
    Year_divid = np.linspace(len(DIVID)-1,0,len(DIVID))
    droite = sc.linregress(Year_divid, DIVID)
    prog_divid = droite.slope / np.mean(DIVID)
    Divid = DIVID[0]

    #Cours
    s = Stock(ticker)
    cours = s.price

    #DETTE
    DETTE_COURANTE = np.asarray(DETTE_COURANTE)
    DETTE_FOURNISSEUR = np.asarray(DETTE_FOURNISSEUR)
    DETTE_LONG = np.asarray(DETTE_LONG)
    TRESO = np.asarray(TRESO)

    DETTE = (DETTE_COURANTE + DETTE_FOURNISSEUR + DETTE_LONG)
    DETTE_NETTE = DETTE - TRESO

    #ROA
    TOT_ACTIF = np.asarray(TOT_ACTIF)
    ROA = RESULT_NET / TOT_ACTIF
    droite = sc.linregress(Year, ROA)
    prog_ROA = droite.slope / np.mean(ROA)
    ROA = np.mean(ROA)

    #EV/EBITDA
    CAP = capital.replace(',', '')
    try :
        CAP = float(CAP.replace('Bil', '0000'))
    except :
        CAP = float(CAP.replace('Mil', '0'))
    CAP = CAP/1000
    DETTE_NETTE = np.mean(DETTE_NETTE)
    EBITDA = np.mean(EBITDA)
    EV = (CAP - DETTE_NETTE)/EBITDA

    #ROIC
    Capitaux_investi = np.mean(CAPITAUX_PROPRE) + DETTE_NETTE
    ROIC = np.mean(RESULT_NET)/Capitaux_investi

    #Dette/Capitaux propre
    DETTE_Capitaux = np.mean(DETTE)/np.mean(CAPITAUX_PROPRE)

    #PRIX_FUTUR
    PER = 15
    alpha = prog_BPA
    beta = 0.10
    prix_futur = PER * BPA * (1 + alpha)**10
    Price = 0.75 * prix_futur/(1+beta)**10

    table_out = {"Capital" : [capital],
    "Chiffre d'affaire" : [Chiffre_Affaire],
    "BPA" : [BPA],
    "Evolution CA %" : [prog_CA],
    "Evolution Rslt net %" :[prog_RN],
    "Evolution Benef %" : [prog_Benef],
    "Marge Brute" : [Marge_brut],
    "Evolution Marge %" : [prog_MB],
    "Resultat net / CA" : [rslt_CA],
    "Dette long terme / Rslt net" : [Rslt_DetteLong],
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
    "rendement / 5 ans" : [rendement],
    "prog ROA" : [prog_ROA],
    "ROA" : [ROA],
    "ROIC" : [ROIC],
    "EV/EBITDA" : [EV],
    "dette / capitaux propre" : [DETTE_Capitaux],
    "Prix Juste (Futur)" : [Price]}

    return table_out

def Scoring(j):
    point = 0
    rank = 0

    # ROIC
    rank += 1
    if table.loc[j, "ROIC"] >= 0.1:
        point += 1

    # ROA
    rank += 1
    if table.loc[j, "ROA"] >= 0.06:
        point += 1

    # prog ROA
    rank += 1
    if table.loc[j, "ROA"] >= -0.05:
        point += 1

    #EV/EBITDA
    rank += 1
    if table.loc[j, "EV/EBITDA"] <= 10:
        point += 1

    #dette/capitaux propre
    rank += 1
    if table.loc[j, "dette / capitaux propre"] < 0.8:
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

        #dette long terme
    rank += 1
    if table.loc[j, "Dette long terme / Rslt net"] <= 3:
        point += 1


    score = point / rank * 20

    return score

def Score_Dividende(j):
    point = 0
    rank = 0

    rank += 1
    if table.loc[j, "Dividende 15 ans"] == "OK":
        point += 1

    # Capitalisation
    capital = table.loc[j, "Capital"].replace('Bil', '0000000')
    capital = capital.replace("Mil","0000")
    capital = float(capital.replace(',', ''))
    rank += 1
    if capital >= 2000000000:
        point += 1

        # CA
    rank += 1
    if table.loc[j, "Chiffre d'affaire"] >= 10000:
        point += 1

    # Evolution CA
    rank += 1
    if table.loc[j, "Evolution CA %"] >= 0:
        point += 1

    # Evolution Dividende
    rank += 1
    if table.loc[j, "Evolution Dividende %"] > 0:
        point += 1

    # Rendement dividende
    rank += 1
    if table.loc[j, "rendement dividende"] >= 0.03 and table.loc[j, "rendement dividende"] < 0.085:
        point += 1

    # Payout Ratio
    rank += 1
    if table.loc[j, "Payout Ratio"] <= 0.7 and table.loc[j, "Payout Ratio"] > 0:
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
    table.loc[j, "BPA"] = table_out["BPA"]
    table.loc[j, "Evolution Dividende %"] = table_out["Evolution Dividende %"]
    if table.loc[j, "Eligibilité"] != "PEA":
        table.loc[j, "Dividende"] = np.asarray(table_out["Dividende"]) * 0.70
    else:
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

    table.loc[j, "rendement dividende"] = table.loc[j, "Dividende"] / table.loc[j, "cours"]

    table.loc[j, "Dette long terme / Rslt net"] = table_out["Dette long terme / Rslt net"]

    table.loc[j, "ROIC"] = table_out["ROIC"]
    table.loc[j, "EV/EBITDA"] = table_out["EV/EBITDA"]
    table.loc[j, "ROA"] = table_out["ROA"]
    table.loc[j, "prog ROA"] = table_out["prog ROA"]
    table.loc[j, "dette /capitaux propre"] = table_out["dette / capitaux propre"]

    table.loc[j, "Prix Juste (Futur)"] = table_out["Prix Juste (Futur)"]

    return table

def Score_Management(j):
    point = 0
    rank = 0

    rank += 1
    if table.loc[j, "Effet Lindi"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Marque"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Scalabilité"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Brevet"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Pricing Power"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Vision long terme"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Etat non Majoritaire"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Dividende 15 ans"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Désir de croissance"] == "OK":
        point += 1

    rank += 1
    if table.loc[j, "Fiabilité de la direction"] == "OK":
        point += 1

    score = point / rank * 20

    return score


a = input("Souhaites-tu tout mettre à jour ? (Y/N)")

driver = webdriver.Chrome(PATH, options=options)

for j in range(59, len(table)):  #len(table)
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

    score3 = Score_Management(j)
    table.loc[j, "Score management"] = score3

    score_final = (score * 2 + score2 + score3) / 4
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