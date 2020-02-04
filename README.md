# Statapp
## Analyse statistique d'un réseau créé à partir de données Twitter.

Le but de cette étude est de découvrir quels sont les comptes Twitter  << importants >> (sens à définir) dans la transmission de l'information politique, principalement française. 
La partie << scrapping >> s'inspirent des pages de Mark Kay: http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/.  L'analyse statistique à l'aide d'une marche aléatoire a été faite sous R. 

* 1ère étape: récupérer les données twitter grace au script de M.Kay adapté
* 2ème étape: Construction du graphe adapté à la marche aléatoire:
  + Une fois non orienté pour la centralité de second ordre
  + une fois orienté pour le pageranking
* 3ème étape: étude des degrés 


Ordre dans lequel exécuter les scripts python:

* 1- ```python get_followers_ids ``` : permet de récupérer plusieurs couches des followers (et followers des followers) d'un compte de départ
* 2- ```python rename.py ``` : permet de renommer les fichiers pour des raisons de mémoire et de garder les dictionnaires pour passer de leur nouveau nom au compte d'origine            
* 3- ```python graph.py ```  :créer pour chaque graphe associé au compte de départ un csv avec toutes les aretes 
* 4- ```python 2.py ``` : crée un fichier pour chaque compte dans lequel on recense ses voisins dans chaque graphe
* 5- ```python 3.py``` : Pour chaque couple de graphe, on regarde les comptes communs, pour tous ces comptes, on rassemble tous ses voisins au sein d'un seul fichier et on supprimme les fichiers dans les autres graphes pour n'avoir qu'un seul fichier. On a ainsi crée le graphe adapté à la marche aléatoire. 
  
