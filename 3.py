#encoding: utf-8
import numpy as np
import os
import glob
import json
import csv
import pandas as pd
import time
import os, errno
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

list_temp=list(list_names1)

try:
    os.makedirs('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/commun')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for k in list_names1:
    os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/'+k)
    f = glob.glob('*.json')
    np1= np.array(map(lambda i: i[0:-5],f))
    list_temp.remove(k)
    for j in list_temp:
        os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/'+j)
        h = glob.glob('*.json')
        np2= np.array(map(lambda i: i[0:-5],h))
        commun={'commun':list(np.intersect1d(np1,np2,assume_unique=True))}
        os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/commun/')
        with open(j+'_'+k+'.json','w') as outf:
            json.dump(commun,outf)
            outf.close()

list_temp=list(list_names1)
count = 0
for k in list_names1:
    list_temp.remove(k)
    for j in list_temp:
        os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/')
        with open('commun/'+j+'_'+k+'.json', 'r') as outf:
            file=list(json.load(outf)['commun'])
            outf.close()
        for v in file:
            os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/')
            if os.path.exists('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/'+j+'/'+v+'.json') & os.path.exists('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/'+k+'/'+v+'.json'):
                with open(j+'/'+v+'.json','r') as cible:
                    voisins=json.load(cible)["voisins"] #on charge ses voisins dans le graphe de j
                    cible.close()
                with open(k+'/'+v+'.json','r') as cible: #on charge ses voisins dans le graphe de k
                    data=json.load(cible)
                    cible.close()
                #on ajoute les voisins du graphe j dans le fichier ds le graphe k
                data['voisins']=list(np.unique(np.concatenate([np.array(data['voisins']),np.array(voisins)])))
                data['deg']=len(data['voisins'])
                with open(k+'/'+v+'.json','w') as outf:
                    json.dump(data,outf)
                    outf.close()

                os.remove('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_temp/'+j+'/'+v+'.json')




print time.time() -t1
