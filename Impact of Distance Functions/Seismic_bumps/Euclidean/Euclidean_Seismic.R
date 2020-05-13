rm(list=ls())
install.packages("UBL")
install.packages("fastDummies")
library("UBL")
library("fastDummies")

df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Seismic_bumps/seismic.txt",header=T, sep=",")

names(df) <- c("seismic", "seismoacoustic", "shift", "genergy", "gpuls","gdenergy", "gdpuls", "ghazard", "nbumps",
               "nbumps2","nbumps3","nbumps4","nbumps5","nbumps6","nbumps7","nbumps89","energy","maxenergy","class")

normFunc <- function(x){(x - mean(x, na.rm = T))/sd(x, na.rm = T)}
df[4:7] <- apply(df[4:7], 2, normFunc)
df[9:13] <- apply(df[9:13], 2, normFunc)
df[17:18] <- apply(df[17:18], 2, normFunc)

df <- fastDummies::dummy_cols(df)
df$seismic<-NULL
df$seismoacoustic<-NULL
df$shift<-NULL
df$ghazard<-NULL

new_df<-df
new_df$class<-NULL

minorityIndex = which(df$class==1)


dist <- distances("genergy",new_df, "Euclidean")
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
    else if(df[x[j],]$class==1)
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

write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_safe.txt", row.names=FALSE, col.names=FALSE)
write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_boarderline.txt", row.names=FALSE, col.names=FALSE)
write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_rare.txt", row.names=FALSE, col.names=FALSE)
write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Euclidean/abalone_Euclidean_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")

