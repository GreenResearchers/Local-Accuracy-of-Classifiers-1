import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["A1", "A2", "A3", "A4", "A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16",
           "A17","A18","A19","A20","class"]

df = pd.read_csv("credit.data", header=None, names=headers, na_values="?")


#new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["A1", "A3", "A4","A6","A7","A9","A10",
#                                                       "A12","A14","A15","A17","A19","A20"]))
replace_lebels = {"A1":     {"A11":0,"A12":1,"A13":2,"A14":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A3":     {"A30":0,"A31":1,"A32":2,"A33":3,"A34":4}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A4":     {"A40":0,"A41":1,"A410":2,"A42":3,"A43":4,"A44":5,"A45":6,"A46":7,"A48":8,"A49":9}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A6":     {"A61":0,"A62":1,"A63":2,"A64":3,"A65":4}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A7":     {"A71":0,"A72":1,"A73":2,"A74":3,"A75":4}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A9":     {"A91":0,"A92":1,"A93":2,"A94":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A10":     {"A101":0,"A102":1,"A103":2}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A12":     {"A121":0,"A122":1,"A123":2,"A124":3}}
df.replace(replace_lebels, inplace=True)

replace_lebels = {"A14":     {"A141":0,"A142":1,"A143":2}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"A15":     {"A151":0,"A152":1,"A153":2}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"A17":     {"A171":0,"A172":1,"A173":2,"A174":3}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"A19":     {"A191":0,"A192":1}}
df.replace(replace_lebels, inplace=True)
replace_lebels = {"A20":     {"A201":0,"A202":1}}
df.replace(replace_lebels, inplace=True)



nominal_attribute_no=[0,2,3,5,6,8,9,11,13,14,16,18,19]
numeric_attribute_no=[1,4,7,10,12,15,17]
label_attribute_no=20
minority_label=2
majority_label=1
K=[5,7,9,11,13,15,17,19]

std = df[["A2", "A5", "A8", "A11","A13", "A16", "A18"]].std()

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
str="Credit_g:\n"
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
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Credit_g/')

#print(GM_all)
