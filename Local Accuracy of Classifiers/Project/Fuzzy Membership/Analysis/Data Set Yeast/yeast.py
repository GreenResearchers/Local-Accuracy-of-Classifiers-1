import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["name", "mcg", "gvh", "alm", "mit","erl", "pox", "vac", "nuc","class"]

df = pd.read_csv("yeast.data", header=None, names=headers, na_values="?")

df= (df.drop(['name'], 1))

replace_lebels = {"class":     {"CYT": 0, "NUC": 0, "MIT":0, "ME3":0, "ME2":1, "ME1":0,"EXC":0,"VAC":0,"POX":0,"ERL":0}}
df.replace(replace_lebels, inplace=True)

std = df[["mcg", "gvh", "alm", "mit","erl", "pox", "vac", "nuc"]].std()



nominal_attribute_no=[]
numeric_attribute_no=[0,1,2,3,4,5,6,7]
label_attribute_no=8
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
str="Yeast:\n"
#Gmean.write(GM_all,str)
from SelectionOfk.AUC import AUC
#AUC_all=AUC.auc(distances,minority_label,majority_label,K,y)
#AUC.write(AUC_all,str)
from SelectionOfk.Fmeasure import Fmeasure
#Fmeasure_all=Fmeasure.fmeasure(distances,minority_label,majority_label,K,y)
#Fmeasure.write(Fmeasure_all,str)
from MembershipCalculation import subCategoryFinder as s
safe,borderline,rare,outlier=s.subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,7,X,y)
#s.write(safe,borderline,rare,outlier,str)
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Yeast/')

#print(GM_all)
