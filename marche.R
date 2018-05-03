library("jsonlite")
library("stringr")
setwd("C:/Users/Apollinaire/Documents/Statapp")
temp = list.files(pattern="*.json")
B=rep(list(retard=c()),13947)
x=fromJSON("3130.json")
i=1
k=0
while(k==0){
  if(length(B[x$id]$retard)==0){
    B[x$id]$retard[1]=i
  }else{
    c=length(B[x$id]$retard)
    B[x$id]$retard[c+1]=i-sum(B[x$id]$retard)
  } 
  w=sample(x$degre,1)
  y=fromJSON(paste(toString(x$voisins[w]),"json",sep="."))
  r=as.numeric(x$degre)/as.numeric(y$degre)
  u=runif(1)
  if (u<r) x=y
  i=i+1
}
dataExS_json<- toJSON(B, pretty = TRUE)
write(dataExS_json, "retour.json")
