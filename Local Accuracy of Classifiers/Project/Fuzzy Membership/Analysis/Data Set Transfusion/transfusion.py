import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["a1", "a2", "a3", "a4","class"]

df = pd.read_csv("transfusion.data", header=None, names=headers, na_values="?")


std = df[["a1", "a2", "a3", "a4"]].std()



nominal_attribute_no=[]
numeric_attribute_no=[0,1,2,3]
label_attribute_no=4
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
str="Transfusion:\n"
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
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Transfusion/')

#print(GM_all)
