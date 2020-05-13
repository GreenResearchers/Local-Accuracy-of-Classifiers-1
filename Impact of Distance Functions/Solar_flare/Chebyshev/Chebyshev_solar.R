
rm(list=ls())
#install.packages("UBL")
#install.packages("fastDummies")
library("UBL")
library("fastDummies")

df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Solar_flare/solar.txt",header=T, sep=",")

names(df) <- c("class", "large_spot", "spot_distribute", "activity", "evolution","previous","historic",
               "sun_disk","area","area_large-spot","c-class","m_class","x_class")

new_df<-df
new_df$class<-NULL

normFunc <- function(x){(x - mean(x, na.rm = T))/sd(x, na.rm = T)}
new_df[3] <- apply(new_df[3], 2, normFunc)
new_df[6:12] <- apply(new_df[6:12], 2, normFunc)



new_df <- fastDummies::dummy_cols(new_df)
new_df$large_spot<-NULL
new_df$spot_distribute<-NULL


minorityIndex = which(df$class=="F")


dist <- distances("sun_disk",new_df, "Chebyshev")
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
    else if(df[x[j],]$class=="F")
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


write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Chebyshev/abalone_Chebyshev_safe.txt", row.names=FALSE, col.names=FALSE)
write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Chebyshev/abalone_Chebyshev_boarderline.txt", row.names=FALSE, col.names=FALSE)
write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Chebyshev/abalone_Chebyshev_rare.txt", row.names=FALSE, col.names=FALSE)
write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Chebyshev/abalone_Chebyshev_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/Chebyshev/abalone_Chebyshev_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")

