import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["buying", "ment", "doors", "persons", "lug_boot","safety", "class"]

df = pd.read_csv("car.data", header=None, names=headers, na_values="?")


replace_lebels = {"class":     {"unacc": 0, "acc": 0, "vgood":0, "good":1}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"buying":     {"vhigh":0,"high":1,"med":2,"low":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"ment":     {"vhigh":0,"high":1,"med":2,"low":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"doors":     {"2":0,"3":1,"4":2,"5more":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"persons":     {"2":0,"4":1,"more":2}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"lug_boot":     {"small":0,"med":1,"big":2}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"safety":     {"low":0,"med":1,"high":2}}
df.replace(replace_lebels, inplace=True)




nominal_attribute_no=[0,1,2,3,4,5]
numeric_attribute_no=[]
label_attribute_no=6
minority_label=1
majority_label=0
K=[5,7,9,11,13,15,17,19]

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
str="Car:\n"
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
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Car/')

#print(GM_all)
