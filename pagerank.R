library("jsonlite")
library("stringr")
library(R.utils)
setwd("C:/Users/Apollinaire/Documents/Pagerank")
temp = list.files(pattern="*.json")
B=rep(list(retour=c()),13947)
x=fromJSON("3130.json")
i=1
k=1
d=0.8
#Implémentation de la marche aléatoire
while(k!=21050000){
  if(length(B[x$id]$retour)==0){
    B[x$id]$retour[1]=i
  }else{
    c=length(B[x$id]$retour)
    B[x$id]$retour[c+1]=i-sum(B[x$id]$retour)
  } 
  u=runif(1)
  if (u<1-d || x$degre==0){
    w=sample(length(temp),1)
    y=fromJSON(temp[w])
  }
  else{
    w=sample(x$degre,1)
    y=fromJSON(paste(toString(x$voisins[w]),"json",sep="."))
  }
  x=y
  i=i+1
  k=k+1
}
#On sauvegarde les temps de retour
dataExS_json<- toJSON(B, pretty = TRUE)
write(dataExS_json, "pagerank.json")
B=read_json("pagerank.json")
moyenne=rep(0,13487)
#Calcul de l'estimateur de la moyenne du temps de retour
for(i in 1:13947){
  if(length(B[[i]])!=0){
    w=as.numeric(B[[i]])
    moyenne[j]=mean(w)
    j=j+1
  }
}
write.csv(moyenne,"moyenne.csv")
h=read.csv("moyenne.csv")
b=as.data.frame(h)
#On ordonne les temps de retour moyens 
b=b[order(b[,2]),]
#On obtient un estimateur moyen de la probabilité invariante
a=1/b[,2]
write.csv(a,"centralite_pagerank.csv")
passage3=rep(0,13487)
#On telecharge le dictionnaire contenant les ids de comptes de twitter des noeuds
e=fromJSON("numtoid.json")
for(k in 1:13487){
  passage3[k]=e[b[k,1]]
}
write.csv(passage3,"Pagerank_numero_fichier")
