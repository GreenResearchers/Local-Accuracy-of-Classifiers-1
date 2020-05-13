
import All_attribute_value_probability_calculation as pc
import Distance_numeric_attributes as dnu
import Distance_nominal_attributes as dno

import collections
import math
#HVDM metric implimentation


##Calculating nominal values required for HVDM calculation, this will calculat all sum off differences in probabilities
# corrosponding to each output class for every attribute that might occour in a dataset and will later be used in VDM part
def calculations(df,headers,nominal_attribute_no,label_attribute_no):
    indexed_sum_sqrd_difference, indexed_elements = pc.attributes_value_probability_calculator(df,headers,nominal_attribute_no,label_attribute_no)
    return indexed_sum_sqrd_difference, indexed_elements

#Calculate distance between two sample
def HVDM(indexed_sum_sqrd_difference,indexed_elements,nominal_attribute_no,numeric_attribute_no,std,a, b):
    z=dnu.numeric_distance(numeric_attribute_no,std,a,b)
    sqr_std_dist_col_nominal=dno.nominal_distance(nominal_attribute_no,indexed_elements,indexed_sum_sqrd_difference,a,b)
    return math.sqrt(z + sqr_std_dist_col_nominal)




