import pandas as pd
import  numpy as np
from HVDM import HVDM as h
import os

from SelectionOfk.Gmean import Gmean
#Preparing data, setting headers
headers = ["c_thickness","uni_cel_size","uni_cel_shape","mer_adher","single_epi_cel_size","bare_nuc","bland_cro",
           "normal_nuec","mitosis","class"]

df = pd.read_csv("breast-w.data", header=None, names=headers, na_values="?")
df=df.fillna(100)

df['class'].replace(
    to_replace=["benign"],
    value=2,
    inplace=True
)
df['class'].replace(
    to_replace=["malignant"],
    value=4,
    inplace=True
)

#new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["A1", "A3", "A4","A6","A7","A9","A10",
#                                                       "A12","A14","A15","A17","A19","A20"]))

nominal_attribute_no=[]
numeric_attribute_no=[0,1,2,3,4,5,6,7,8]
label_attribute_no=9
minority_label=4
majority_label=2
K=[5,7,9,11,13,15,17,19]

std = df[["c_thickness","uni_cel_size","uni_cel_shape","mer_adher","single_epi_cel_size","bare_nuc","bland_cro",
           "normal_nuec","mitosis"]].std()

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
str="Breast W:\n"
#Gmean.write(GM_all,str)
from SelectionOfk.AUC import AUC
#AUC_all=AUC.auc(distances,minority_label,majority_label,K,y)
#AUC.write(AUC_all,str)
from SelectionOfk.Fmeasure import Fmeasure
#Fmeasure_all=Fmeasure.fmeasure(distances,minority_label,majority_label,K,y)
#Fmeasure.write(Fmeasure_all,str)
from MembershipCalculation import subCategoryFinder as s
safe,borderline,rare,outlier=s.subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,19,X,y)
#s.write(safe,borderline,rare,outlier,str)
s.write_separetely(safe,borderline,rare,outlier,'C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/Analysis/Data Set Breast_w/')

#print(GM_all)
