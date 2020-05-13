import numpy as np
def fuzzyMembership(sorted_k_distances,neighbour_weights,y,minority_label,k):

    count =0
    b=2.0
    fuzzy_membership_coefficient1_total=0
    fuzzy_membership_coefficient_divident_sum=0
    while (count<k):
        weight=0
        if(neighbour_weights[count]==0):
            weight=0.001
        else:
            weight=neighbour_weights[count]
        membership=0
        if (y[sorted_k_distances[count]]==minority_label):
            membership=1
        #similarity=np.absolute(1-neighbour_weights[count])

        fuzzy_membership_coefficient1=1/pow(weight,(2/(b-1)))
        fuzzy_membership_coefficient1_total=fuzzy_membership_coefficient1_total+fuzzy_membership_coefficient1
        fuzzy_membership_coefficient2=membership#*similarity
        fuzzy_membership_coefficient_divident=fuzzy_membership_coefficient2*fuzzy_membership_coefficient1
        fuzzy_membership_coefficient_divident_sum=fuzzy_membership_coefficient_divident_sum+fuzzy_membership_coefficient_divident
        count=count+1
    fuzzy_membership=fuzzy_membership_coefficient_divident_sum/fuzzy_membership_coefficient1_total
    return fuzzy_membership
