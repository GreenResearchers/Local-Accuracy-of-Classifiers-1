import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["name","class","id","rasc","dec","sca","bb1","bb2","rb1","rb2","a1", "a2", "a3", "a4", "a5","a6", "a7", "a8",
           "a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19","a20","a21","a22","a23","a24","a25","a26",
           "a27","a28","a29","a30","a31","a32","a33","a34","a35","a36","a37","a38", "a39", "a40", "a41", "a42","a43", "a44", "a45",
           "a46","a47","a48","a49","a50","a51","a52","a53","a54","a55","a56","a57","a58","a59","a60","a61","a62","a63",
           "a64","a65","a66","a67","a68","a69","a70","a71","a72","a73","a74","a75","a76","a77","a78","a79","a80","a81",
           "a82","a83","a84","a85","a86","a87","a88","a89","a90","a91","a92","a93"]

df = pd.read_csv("spectometer.data", header=None, names=headers, na_values="?")
df= (df.drop(['name'], 1))
df= (df.drop(['id'], 1))
df= (df.drop(['rasc'], 1))
df= (df.drop(['dec'], 1))
df= (df.drop(['sca'], 1))
df= (df.drop(['bb1'], 1))
df= (df.drop(['bb2'], 1))
df= (df.drop(['rb1'], 1))
df= (df.drop(['rb2'], 1))
headers = [ "a1", "a2", "a3", "a4", "a5","a6", "a7", "a8",
           "a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19","a20","a21","a22","a23","a24","a25","a26",
           "a27","a28","a29","a30","a31","a32","a33","a34","a35","a36","a37","a38", "a39", "a40", "a41", "a42","a43", "a44", "a45",
           "a46","a47","a48","a49","a50","a51","a52","a53","a54","a55","a56","a57","a58","a59","a60","a61","a62","a63",
           "a64","a65","a66","a67","a68","a69","a70","a71","a72","a73","a74","a75","a76","a77","a78","a79","a80","a81",
           "a82","a83","a84","a85","a86","a87","a88","a89","a90","a91","a92","a93","class"]
new_order = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
             48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,
            83,84,85,86,87,88,89,90,91,92,93,0]
df = df[df.columns[new_order]]






std = df[["a1", "a2", "a3", "a4", "a5","a6", "a7", "a8",
           "a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19","a20","a21","a22","a23","a24","a25","a26",
           "a27","a28","a29","a30","a31","a32","a33","a34","a35","a36","a37","a38", "a39", "a40", "a41", "a42","a43", "a44", "a45",
           "a46","a47","a48","a49","a50","a51","a52","a53","a54","a55","a56","a57","a58","a59","a60","a61","a62","a63",
           "a64","a65","a66","a67","a68","a69","a70","a71","a72","a73","a74","a75","a76","a77","a78","a79","a80","a81",
           "a82","a83","a84","a85","a86","a87","a88","a89","a90","a91","a92","a93"]].std()



df['class'] = df['class'].mask(df['class'] < 44, 0)
df['class'] = df['class'].mask(df['class'] >=44, 1)

nominal_attribute_no=[]
numeric_attribute_no=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,
                      38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,
                      71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92]
label_attribute_no=93
minority_label=1
majority_label=0
K=[5,7,9,11,13,15,17,19]


indexed_sum_sqrd_difference, indexed_elements=h.calculations(df,headers,nominal_attribute_no,label_attribute_no)


X = np.array(df.drop(['class'], 1))
y = np.array(df['class'])

distances=[]
for a in X:
    distance=[]
    for b in X:
        data=h.HVDM(indexed_sum_sqrd_difference,indexed_elements,nominal_attribute_no,numeric_attribute_no,std,a, b)
        distance.append(data)
    distances.append(distance)
        #print(distances)

#Calculate the Gmeans
#GM_all=Gmean.gmean(distances,minority_label,majority_label,K,y)
#Write the data into file
str="Spectometer:\n"
#Gmean.write(GM_all,str)
from SelectionOfk.AUC import AUC
#AUC_all=AUC.auc(distances,minority_label,majority_label,K,y)
#AUC.write(AUC_all,str)
from SelectionOfk.Fmeasure import Fmeasure
#Fmeasure_all=Fmeasure.fmeasure(distances,minority_label,majority_label,K,y)
#Fmeasure.write(Fmeasure_all,str)
from MembershipCalculation import subCategoryFinder as s
safe,borderline,rare,outlier=s.subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,5,X,y)
#s.write(safe,borderline,rare,outlier,str)
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Spectometer/')

#print(GM_all)
