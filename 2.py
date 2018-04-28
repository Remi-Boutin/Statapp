#encoding: utf-8
import numpy as np
import os
import glob
import json
import csv
import pandas as pd
import time
import os, errno
import re
import ast
import yaml

dossier=[path]

#le script cree des fichiers txt du style journal1_journal2.txt
#dans lequel il y a tous les comptes qui appartiennent a la fois au graphe
#du journal1 et du graphe du journal2
t1= time.time()

list_names=['CNEWS','Europe1','FN_Officiel','Le_Figaro','lemonde','lesRepublicains','partisocialiste',
'BFMTV','Challenges','EnMarchefr','FranceInsoumise','LesEchos',
'MarianneleMag','RTLFrance']

list_names1=['CNEWS','Europe1','FN_Officiel','Le_Figaro','lemonde','lesRepublicains','partisocialiste',
'Challenges','EnMarchefr','FranceInsoumise','LesEchos',
'MarianneleMag','RTLFrance']


with open(dossier+'idtonum.json') as outf:
    idtonum=yaml.load(json.dumps(json.load(outf)))
    outf.close()

with open(dossier+'numtoid.json') as outf:
    numtoid=yaml.load(json.dumps(json.load(outf)))
    outf.close()

def ngb_select(id):
    try:
        return idtonum[str(id)] #si il est dans les fichiers, on le met dans le graphe
    except KeyError as e:
        return -1
         #sinon on continue

for j in list_names1:
    print j
    #on charge le csv contenant tous les liens du graphe
    df=pd.read_csv(dossier+'twitter_network/'+j+'_network.csv',names = ['A','B','C'],engine='python')
    os.chdir(dossier+'twitter-users/'+j)
    print df.head()
    f = glob.glob('*.json')
    #on recupere toutes les noeuds lies au compte
    np1 = np.append(np.array(df['A']),np.array(df['B']))
    np1= np.unique(np1)
    np2=[]
    #on garde que ceux dans le graphe et on enleve ceux qui ne sont pas dans les dictionnaires (du fait qu'on a ete une etape trop loin)
    for i in np1:
        try:
            t=idtonum[str(i)]
            np2.append(idtonum[str(i)])
        except KeyError:
            continue
    np1=np.array(np2)
    #on cree un dictionnaire ou l'on met tous les voisins d'un compte puis on met ce dictionnaire dans un fichier json qui porte le nom du compte
    for i in np1:
        ngbs =  np.append(np.array(df[df['A']==int(numtoid[str(i)])]['B']), np.array(df[df['B']==int(numtoid[str(i)])]['A']))
        ngbs = np.unique(ngbs)
        ngbs = map(ngb_select, list(ngbs))
        dico = {'voisins': ngbs, 'deg' : 0 }
        try:
            os.makedirs(dossier+'/compte_temp/'+j)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(dossier+'compte_temp/'+j+'/'+str(i)+'.json', 'w') as outf:
            json.dump(dico, outf)
            outf.close()
print time.time() - t1
