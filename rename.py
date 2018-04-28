#encoding: utf-8

#amazing idea from Cyril Wheisang.
#on renomme tous les fichier de 1 a n et on cree des dictionnaires
#pour passer du nouveau nom a l'id et inversement

import os
import glob
import numpy as np
import json
import time
import yaml


t1= time.time()
#sous dossiers dans lesquels sont stockes tous les comptes
list_names=['CNEWS','Europe1','FN_Officiel','Le_Figaro','lemonde','lesRepublicains','partisocialiste','Challenges','EnMarchefr','FranceInsoumise','LesEchos',
'MarianneleMag','RTLFrance']
real_name=list()

#on met tous les comptes les uns a la suite des autres dans la list real_name
for k in list_names:
    os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/twitter-users/'+k)
    f = glob.glob('*.json')
    real_name.extend(map(lambda i: i[0:-5], f))

rn_array=np.array(real_name)
rn_array=np.unique(rn_array)

print rn_array.size
print len(rn_array)
os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/')

#dictionnaire qui d'un numero renvoie l'id de depart
dico={i:rn_array[i] for i in range(0,len(rn_array))}
with open("numtoid.json",'w') as outf:
    json.dump(dico, outf)
    outf.close()
#dictionnaire qui d'un id renvoie le nouveau numero
dico={rn_array[i]:i for i in range(0,len(rn_array))}
with open("idtonum.json",'w') as outf:
    json.dump(dico, outf)
    outf.close()

#on renomme les fichiers avec leur nouveau nom
for  h in list_names:
    os.chdir('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/twitter-users/'+h)
    f = glob.glob('*.json')
    real_name = map(lambda i: i[0:-5], f)
    for k in f:
        d=dico[k[0:-5]]
        os.rename(k, str(d)+'.json' )

with open('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/idtonum.json') as outf:
    dico=yaml.load(json.dumps(json.load(outf)))
    outf.close()

with open('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_id.json') as outf:
    compte=yaml.load(json.dumps(json.load(outf)))
    outf.close()

for k in range(1,15):
    compte[str(k)]=dico[str(compte[str(k)])]

with open('C:/Users/remib/Documents/ENSAE/2A/Statapp/graph/compte_id_edit.json','w') as outf:
    json.dump(compte,outf)
    outf.close()
print time.time() - t1
