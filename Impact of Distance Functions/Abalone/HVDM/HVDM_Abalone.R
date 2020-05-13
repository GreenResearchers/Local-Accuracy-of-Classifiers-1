
install.packages("UBL")
rm(list=ls())
library("UBL")
df <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/abalone.txt",header=T, sep=",")

col_idx <- grep("rings", names(df))
df <- df[, c(col_idx, (1:ncol(df))[-col_idx])]

normFunc <- function(x){(x - mean(x, na.rm = T))/sd(x, na.rm = T)}
df[3:9] <- apply(df[3:9], 2, normFunc)
new_df<-df
new_df$rings<-NULL

dist <- distances("sex",new_df, "HVDM")
#write.table(dist, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_distances.txt", row.names=FALSE, col.names=FALSE,sep=" ")

#dist <- read.table(file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_distances.txt",header=F, sep=" ")
#print(dist)

minorityIndex = which((df$rings>=0 & df$rings<=4)|(df$rings>=16 & df$rings<=29))


neighbours <- t(apply(dist, 1, order)[ 1:6,])
#print(neighbours)
#write.table(neighbours, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_neighbours.txt", row.names=FALSE, col.names=FALSE)

safe = list()
boarderline = list()
rare = list()
outlier = list()

for (i in minorityIndex) {
  x = neighbours[i,]
  majorCount <- 0
  minorCount <- 0
  
  j = 1
  while(j<=6){
    if(x[j]==i){
      minorCount = minorCount
      majorCount = majorCount
    }
    else if((df[x[j],]$rings>=0 & df[x[j],]$rings<=4)|(df[x[j],]$rings>=16 & df[x[j],]$rings<=29))
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

write.table(safe, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_safe.txt", row.names=FALSE, col.names=FALSE)
write.table(boarderline, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_boarderline.txt", row.names=FALSE, col.names=FALSE)
write.table(rare, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_rare.txt", row.names=FALSE, col.names=FALSE)
write.table(outlier, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_outlier.txt", row.names=FALSE, col.names=FALSE)

x <- data.frame("safe" = c(length(safe)), "boarderline" = c(length(boarderline)),"rare" = c(length(rare)),"outlier" = c(length(outlier)))
write.table(x, file="C:/Users/Mahin/Google Drive/Workspace/Impact of Distance Functions/Abalone/HVDM/abalone_HVDM_subconcepts.txt", row.names=FALSE, col.names=T,sep=",")
