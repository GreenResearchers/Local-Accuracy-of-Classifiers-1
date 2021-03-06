rm(list=ls())
install.packages("UBL")
install.packages("fastDummies")
library("UBL")
library("fastDummies")


df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Nursery/nursary.txt",header=F, sep=",")

names(df) <- c("parents", "has_nurs", "form", "children", "housing","finance","social","health","class")

df <- fastDummies::dummy_cols(df)
df$parents<-NULL
df$has_nurs<-NULL
df$form<-NULL
df$children<-NULL
df$housing<-NULL
df$finance<-NULL
df$social<-NULL
df$health<-NULL

new_df<-df
new_df$class<-NULL

dist <- distances("children_1",new_df, "Manhattan")

minorityIndex = which(df$class=="very_recom")


safe = list()
boarderline = list()
rare = list()
outlier = list()

for(item in minorityIndex) {
  
  #write.table(neighbours, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_neighbours.txt", row.names=FALSE, col.names=FALSE)
  distances=dist[item,]
  neighbours <- sort(distances,index.return=T)$ix
  neighbours <- neighbours[2:6]
  
  majorCount <- 0
  minorCount <- 0
  
  j = 1
  while(j<6){
    if(df[neighbours[j],]$class=="very_recom")
      minorCount = minorCount + 1
    else
      majorCount = majorCount + 1
    j = j + 1
  }
  
  if((majorCount==0 & minorCount==5)|(majorCount==1 & minorCount==4))
    safe <- c(safe,item)
  
  else if((majorCount==2 & minorCount==3)|(majorCount==3 & minorCount==2))
    boarderline <- c(boarderline,item)
  
  else if(majorCount==4 & minorCount==1)
    rare <- c(rare,item)
  else
    outlier <- c(outlier,item)
}

write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_safe.txt", row.names=FALSE, col.names=FALSE)
write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_boarderline.txt", row.names=FALSE, col.names=FALSE)
write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_rare.txt", row.names=FALSE, col.names=FALSE)
write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")

