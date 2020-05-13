import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
from SelectionOfk.AUC import AUC

#Preparing data, setting headers
headers = ["class","l_weight","l_distance","r_weight","r_distance"]

df = pd.read_csv("balance-scale.data", header=None, names=headers, na_values="?")

replace_lebels = {"class":     {"L": 0, "R": 0, "B":1}}
df.replace(replace_lebels, inplace=True)
df= df[["l_weight","l_distance","r_weight","r_distance","class"]]
headers = ["l_weight","l_distance","r_weight","r_distance","class"]
nominal_attribute_no=[0,1,2,3]
numeric_attribute_no=[]
label_attribute_no=4
minority_label=1
majority_label=0
K=[5,7,9,11,13,15,17,19]

max_value = df[[]].max()
min_value = df[[]].min()
std = df[[]].std()

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
str="Balance Scale:\n"
#Gmean.write(GM_all,str)

#AUC_all=AUC.auc(distances,minority_label,majority_label,K,y)
#AUC.write(AUC_all,str)
from SelectionOfk.Fmeasure import Fmeasure
#Fmeasure_all=Fmeasure.fmeasure(distances,minority_label,majority_label,K,y)
#Fmeasure.write(Fmeasure_all,str)
from MembershipCalculation import subCategoryFinder as s
safe,borderline,rare,outlier=s.subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,5,X,y)
#s.write(safe,borderline,rare,outlier,str)
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set BalanaceScale/')

#print(GM_all)
