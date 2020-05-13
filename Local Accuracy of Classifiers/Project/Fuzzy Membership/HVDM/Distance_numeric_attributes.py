def numeric_distance(numeric_attribute_no,std,a,b):
    z=0
    count=0
    for attribute in numeric_attribute_no:
        normalized_diff = (a[attribute] - b[attribute]) / (4*std[count])
        normalized_diff=normalized_diff*normalized_diff
        z=normalized_diff+z
        count=count+1
    return z
