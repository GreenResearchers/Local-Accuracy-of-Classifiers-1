rm(list=ls())
install.packages("UBL")
install.packages("fastDummies")
library("UBL")
library("fastDummies")

df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Balance_scale/balance-scale.txt",header=T, sep=",")
names(df) <- c("class","A1", "A2", "A3", "A4")

normFunc <- function(x){(x - mean(x, na.rm = T))/sd(x, na.rm = T)}
df[2:5] <- apply(df[2:5], 2, normFunc)

new_df<-df
new_df$class<-NULL


dist <- distances("A1",new_df, "Manhattan")
#write.table(dist, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_distances.txt", row.names=FALSE, col.names=FALSE)
neighbours <- t(apply(dist, 1, order)[ 1:6, ])
#write.table(neighbours, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_neighbours.txt", row.names=FALSE, col.names=FALSE)
neighbours <- neighbours[,2:6]




minorityIndex = which(df$class=="B")


safe = list()
boarderline = list()
rare = list()
outlier = list()

for (i in minorityIndex) {
  x = neighbours[i,]
  majorCount <- 0
  minorCount <- 0
  
  j = 1
  while(j<6){
    if(df[x[j],]$class=="B")
      minorCount = minorCount + 1
    else
      majorCount = majorCount + 1
    #print(x[j])
    j = j + 1
  }
  
  if((majorCount==0 & minorCount==5)|(majorCount==1 & minorCount==4))
    safe <- c(safe,i)
  
  else if((majorCount==2 & minorCount==3)|(majorCount==3 & minorCount==2))
    boarderline <- c(boarderline,i)
  
  else if(majorCount==4 & minorCount==1)
    rare <- c(rare,i)
  else
    outlier <- c(outlier,i)
}

write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Manhattan/abalone_Manhattan_safe.txt", row.names=FALSE, col.names=FALSE)
write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Manhattan/abalone_Manhattan_boarderline.txt", row.names=FALSE, col.names=FALSE)
write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Manhattan/abalone_Manhattan_rare.txt", row.names=FALSE, col.names=FALSE)
write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Manhattan/abalone_Manhattan_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Manhattan/abalone_Manhattan_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")

