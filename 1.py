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


with open('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/idtonum.json') as outf:
    idtonum=yaml.load(json.dumps(json.load(outf)))
    outf.close()

with open('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/numtoid.json') as outf:
    numtoid=yaml.load(json.dumps(json.load(outf)))
    outf.close()

count = 0
list_temp=list(list_names1)

for k in list_names1:
    os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/twitter-users/'+k)
    f = glob.glob('*.json')
    np1= np.array(map(lambda i: i[0:-5],f))
    list_temp.remove(k)
    #on regarde dans tous les autres graphes si le compte est present
    for j in list_temp:
        os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/twitter-users/'+j)
        #on cree un fichier qui donne les comptes communs entre deux graphes, pour chaque couple de graphes
        h = glob.glob('*.json')
        np2= np.array(map(lambda i: i[0:-5],h))
        commun={'commun':list(np.intersect1d(np1,np2,assume_unique=True))}
        os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/commun')
        with open(j+'_'+k+'.json','w') as outf:
            json.dump(commun,outf)
            outf.close()
