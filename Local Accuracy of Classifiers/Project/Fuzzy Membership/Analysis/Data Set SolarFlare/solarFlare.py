import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
old_headers = ["class", "large_spot", "spot_distribute", "activity", "evolution","previous","historic",
           "sun_disk","area","area_large-spot","c-class","m_class","x_class"]

df = pd.read_csv("solar.data", header=None, names=old_headers, na_values="?")
replace_lebels = {"class":     {"F": 1, "A":0,"B":0,"C":0,"D":0,"E":0,"H":0}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"large_spot":     {"A": 0, "H":1,"K":2,"R":3,"S":4,"X":5}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"spot_distribute":     {"C": 0, "I":1, "O":2, "X":3}}
df.replace(replace_lebels, inplace=True)

headers = [ "large_spot", "spot_distribute", "activity", "evolution","previous","historic",
           "sun_disk","area","area_large-spot","c-class","m_class","x_class","class"]
new_order = [1,2,3,4,5,6,7,8,9,10,11,12,0]
df = df[df.columns[new_order]]

nominal_attribute_no=[0,1,2,3,4,5,6,7,8,9,10,11]
numeric_attribute_no=[]
label_attribute_no=12
label="class"
minority_label=1
majority_label=0
K=[5,7,9,11,13,15,17,19]
#
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
str="Solar Flare:\n"
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
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set SolarFlare/')

#print(GM_all)
