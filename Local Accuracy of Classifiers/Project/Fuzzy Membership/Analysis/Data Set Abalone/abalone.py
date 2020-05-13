import pandas as pd
import  numpy as np
from HVDM import HVDM as h

from SelectionOfk.Gmean import Gmean
from SelectionOfk.AUC import AUC
#Preparing data, setting headers
headers = ["sex", "length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight", "rings"]

#reading data from csv
df = pd.read_csv("abalone.data", header=None, names=headers, na_values="?")

#replacing nominal data to numeric values
replace_lebels = {"sex":     {"M": 0, "F": 1, "I":2}}
df.replace(replace_lebels, inplace=True)

df['rings'].replace(
    to_replace=[0, 1,2,3,4,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
    value=20,
    inplace=True
)
df['rings'].replace(
    to_replace=[5,6,7,8,9,10,11,12,13,14,15],
    value=10,
    inplace=True
)

#listing nominal attribute and numeric attributes will seperate the calculation
nominal_attribute_no=[0]
numeric_attribute_no=[1,2,3,4,5,6,7]
#Labels will be required for separeting minority data and HVDM calculation as frequency of different class is needed
label_attribute_no=8
minority_label=20
majority_label=10

K=[5,7,9,11,13,15,17,19]
#K=[5]

# Calculating standard deviation of different attributes for the HVDM metric
new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["sex"]))

max_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].max()
min_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].min()

std = df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].std()

indexed_sum_sqrd_difference, indexed_elements=h.calculations(df,headers,nominal_attribute_no,label_attribute_no)


X = np.array(df.drop(['rings'], 1))
y = np.array(df['rings'])

#Calculate distances of the whole dataset
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
str="Abalone:\n"
#Gmean.write(GM_all,str)

#AUC_all=AUC.auc(distances,minority_label,majority_label,K,y)
#AUC.write(AUC_all,str)
from SelectionOfk.Fmeasure import Fmeasure
#Fmeasure_all=Fmeasure.fmeasure(distances,minority_label,majority_label,K,y)
#Fmeasure.write(Fmeasure_all,str)
from MembershipCalculation import subCategoryFinder as s
safe,borderline,rare,outlier=s.subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,5,X,y)
#s.write(safe,borderline,rare,outlier,str)
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Abalone/')
