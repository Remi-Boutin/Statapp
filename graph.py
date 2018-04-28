# -*- coding: utf-8 -*-
import glob
import os
import json
import sys
from collections import defaultdict
import yaml
import time
t1= time.time()

dossier=[path]
#But de ce script: creer le csv contenant tous les liens du graph d'un parti ou d'un media
os.chdir(dossier)
users = defaultdict(lambda: { 'followers': 0 })

dico={1:'CNEWS',2:'Europe1',3:'FN_Officiel',4:'Le_Figaro',5:'lemonde',6:'lesRepublicains',7:'partisocialiste',
8:'BFMTV',9:'Challenges',10:'EnMarchefr',11:'FranceInsoumise',12:'LesEchos',
13:'MarianneleMag',14:'RTLFrance'}

print dico
var=input('Entrer le media ou parti qui vous interesse : ')


with open('idtonum.json','r') as outf:
    num=yaml.load(json.dumps(json.load(outf)))
    outf.close()

with open('numtoid.json','r') as outf:
    numtoid=yaml.load(json.dumps(json.load(outf)))
    outf.close()

with open('compte_id_edit.json','r') as outf:
    data=json.load(outf) #on ouvre le dico qui stocke les ids
SEED= data[str(var)] #on charge le compte central id de type int

for f in glob.glob('twitter-users/'+dico[var]+'/*.json'):
    data = json.load(file(f))
    screen_name = num[str(data['id'])]
    users[screen_name] = { 'followers': data['followers_count'] }

def process_follower_list(screen_name, edges=[], depth=0, max_depth=2):
    #pour le compte screen_name
    #on va dans le fichier, on regarde ses followers pour creer le lien
    f = os.path.join('twitter-users/'+dico[var]+'/'+ str(screen_name) + '.json')

    if not os.path.exists(f):
        return edges

    with open(f) as json_data:
        data = json.load(json_data)
    followers = data['followers_ids']
    for follower in followers:
        print follower
        try:
            screen_name_2 = num[str(follower)]
        except:
            num[str(follower)]=len(num.keys())
            numtoid[str(len(numtoid.keys()))]=str(follower)
            screen_name_2 = num[str(follower)]
        # utilise le nombre de follower de screen_name comme poid de l'arete
        weight = users[screen_name]['followers']
        edges.append([str(screen_name), str(screen_name_2), str(weight)])
        #on ne va pas plus loins que 2 profondeurs apres le compte de depart
        if depth+1 < max_depth:
            process_follower_list(screen_name_2, edges, depth+1, max_depth)
    return edges
edges = process_follower_list(SEED, max_depth=3)

#on met le tout dans le csv
with open('twitter_network/'+dico[var]+'_network.csv', 'w') as outf:
    edge_exists = {}
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not(key in edge_exists):
            outf.write('%s,%s,%s\n' % (edge[0], edge[1], edge[2]))
            edge_exists[key] = True
print time.time() - t1
