def nominal_distance(nominal_attribute_no,indexed_elements,indexed_sum_sqrd_difference,a,b):
    sqr_std_dist_col_nominal=0

    for attribute in nominal_attribute_no:
        sqr_std_dist_col=0
        if a[attribute] == b[attribute]:
            sqr_std_dist_col = 0
        else:
            elements=[]
            for element in indexed_elements:
                if element[0]==attribute:
                    elements=element[1]
            sum_sqrd_differences=[]
            for sum_sqrd_difference in indexed_sum_sqrd_difference:
                if sum_sqrd_difference[0]==attribute:
                    sum_sqrd_differences=sum_sqrd_difference[1]
            for element1 in elements:
                for element2 in elements:
                    if(element1!=element2):
                        for diffrence in sum_sqrd_differences:
                            if diffrence[0]==element1 and diffrence[1]==element2:
                                sqr_std_dist_col = diffrence[2]
                            else:
                                sqr_std_dist_col = 1
        sqr_std_dist_col_nominal=sqr_std_dist_col_nominal+sqr_std_dist_col
    return sqr_std_dist_col_nominal
