library("jsonlite")
library("R.utils")
#On charge le fichier contenant tous les temps de retours associ?s aux noeuds de la marche
n=fromJSON("retour.json")
retour=rep(0,13947)
# On calcule l'estimateur de la centralit? du second ordre pour chaque noeud
retour[1]=sqrt((sum(n[[1]]^2))/(length(n[[1]])-1)-(sum(n[[1]])/(length(n[[1]])-1))^2)
for(i in 2:13947){
  if(length(n[[i]])!=0){
  retour[i]=sqrt(((sum(n[[i]]^2))/(length(n[[i]])-1))-(sum(n[[i]])/(length(n[[i]])-1))^2)
  }
}
#On sauvegarde le fichier contenant les estimateurs
write.csv(retour,"centralite.csv")
t=read.csv("centralite.csv")
#On s'interesse aux noeuds ayant des estimateurs faibles ainsi on range le tableau des estimateurs dans l'ordre croissant
tab=as.data.frame(t)
tab=tab[order(tab[,2]),]
#On sauvegarde ce nouveau tableau
write.csv(tab,"centralite_ordonne.csv")
tab1=read.csv("centralite_ordonne.csv")
position=rep(0,13486)
i=1
x=tab1[[3]]
p=tab1[[2]]
#On retrouve a quel noeud est associe un estimateur dans le tableau ordonn?
#On commence a 462 car les estimateurs precedents sont nuls
position=p[462:13947]
write.csv(position,"position.csv")
po=read.csv("position.csv")
position=as.matrix(po[2])
# On calcule le nombre de passages sur un noeud 
#On s'interesse aux 150 noeuds les plus influents selon la centralite du second ordre
j=1
passage1=rep(0,150)
for(k in 1:150){
  a=position[k]
  passage1[j]=length(n[[a]])
  j=j+1
}
write.csv(passage1,"passage_noeuds.csv")
j=1
degre=rep(0,13486)
#On calcule la centralite du premier ordre
for(k in 1:13486){
  a=position[k]-1
  b=paste(a,"json",sep=".")
  c=fromJSON(b)
  degre[j]=c$degre
  j=j+1
}
write.csv(degre,"degre.csv")
#On telecharge le dictionnaire contenant les ids de comptes de twitter des noeuds
e=fromJSON("numtoid.json")
passage2=rep(0,13486)
for(k in 1:13486){
  passage2[k]=e[[position[k]]]
}
#On sauvegarde les numéros initiaux des fichiers avant la transformation du graphe
write.csv(passage2,"numéro_fichier_ordonne")
