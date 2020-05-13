
install.packages("UBL")
rm(list=ls())
library("UBL")
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

new_df<-df
new_df$class<-NULL

dist <- distances("A1",new_df, "HEOM")
#write.table(dist, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_distances.txt", row.names=FALSE, col.names=FALSE)
neighbours <- t(apply(dist, 1, order)[ 1:6,])
#write.table(neighbours, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_neighbours.txt", row.names=FALSE, col.names=FALSE)
neighbours <- neighbours[,2:6]




minorityIndex = which(df$class==2)


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

#write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_safe.txt", row.names=FALSE, col.names=FALSE)
#write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_boarderline.txt", row.names=FALSE, col.names=FALSE)
#write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_rare.txt", row.names=FALSE, col.names=FALSE)
#write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HEOM/abalone_HEOM_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")

