rm(list=ls())
install.packages("UBL")
install.packages("fastDummies")
library("UBL")
library("fastDummies")

df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Credit_g/credit.txt",header=T, sep=",")

names(df) <- c("A1", "A2", "A3", "A4", "A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16",
               "A17","A18","A19","A20","class")
normFunc <- function(x){(x - mean(x, na.rm = T))/sd(x, na.rm = T)}
df[2] <- apply(df[2], 2, normFunc)
df[5] <- apply(df[5], 2, normFunc)
df[8] <- apply(df[8], 2, normFunc)
df[11] <- apply(df[11], 2, normFunc)
df[13] <- apply(df[13], 2, normFunc)
df[16] <- apply(df[16], 2, normFunc)
df[18] <- apply(df[18], 2, normFunc)

df <- fastDummies::dummy_cols(df)
df$A1<-NULL
df$A3<-NULL
df$A4<-NULL
df$A6<-NULL
df$A7<-NULL
df$A9<-NULL
df$A10<-NULL
df$A12<-NULL
df$A14<-NULL
df$A15<-NULL
df$A17<-NULL
df$A19<-NULL
df$A20<-NULL

new_df<-df
new_df$class<-NULL


minorityIndex = which(df$class==2)


dist <- distances("A2",new_df, "Manhattan")
#write.table(dist, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_distances.txt", row.names=FALSE, col.names=FALSE)
neighbours <- t(apply(dist, 1, order)[ 1:6, ])
#write.table(neighbours, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_neighbours.txt", row.names=FALSE, col.names=FALSE)

safe = list()
boarderline = list()
rare = list()
outlier = list()

for(i in minorityIndex) {
  x = neighbours[i,]
  majorCount <- 0
  minorCount <- 0
  
  j = 1
  while(j<=6){
    if(x[j]==i){
      minorCount = minorCount
      majorCount = majorCount
    }
    else if(df[x[j],]$class==2)
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

