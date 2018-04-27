# Statapp
Statistical network analysis

Ces scripts ont été largement inspirés par les pages de Mark Kay: http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/

1ère étape: récupérer les données twitter grace au script de M.Kay adapté
2ème étape: Construction du graphe adapté à la marche aléatoire:
-Une fois non orienté pour la centralité de second ordre
-une fois orienté pour le pageranking
3ème étape: étude des degrés 


Ordre dans lequel exécuter les scripts python:

1- get_followers_ids : permet de récupérer plusieurs couches des followers (et followers des followers) d'un compte de départ
2- rename.py : permet de renommer les fichiers pour des raisons de mémoire et de garder les dictionnaires pour passer de leur nouveau nom
              au compte d'origine
3- graph.py  :créer pour chaque graphe associé au compte de départ un csv avec toutes les aretes 
4- 1.py : crée les fichiers comportant les comptes communs à deux graphes différents
5- 2.py : crée un fichier pour chaque compte dans lequel on recense ses voisins dans chaque graphe
6- 3.py : pour tous les comptes dans plusieurs graphes, on rassemble tous ses voisins au sein d'un seul
          fichier et on supprimme les fichiers dans les autres graphes pour n'avoir qu'un seul fichier au final
  
