from HVDM import HVDM
import numpy as np
import pandas as pd
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
minority_label=50
majority_label=100

# Calculating standard deviation of different attributes for the HVDM metric
new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["sex"]))

max_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].max()
min_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].min()

std = df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].std()

indexed_sum_sqrd_difference, indexed_elements=HVDM.calculations(df,headers,nominal_attribute_no,label_attribute_no)

