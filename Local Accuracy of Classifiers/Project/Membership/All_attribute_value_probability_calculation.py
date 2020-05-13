import numpy as np

# This function will take dataset, headers of the attributes, the nominal attributes numbers within the dataset and
# output label attribute as input and will calculate the sum of all possible difference in probability for every
# two possible values or categories for each attribute for each output label and will return the outputs.
# The idea is, for an attribute there will be a number of nominal vaules, so the probabilities and even difference of
# probabilities can be calculates beforehand. This will reduce calculation in VDM calculation

# Inputs: Dataset, Headers, Nominal attributes numbers, Label attribute number
# Output: Sum of all [P_a_x_c - P_a,y,c]^2 where, a indicates all attributes, x and y indicates two values of a certain
# attribute and c indicates all possible output classes or, VDM equation for every attribute
def attributes_value_probability_calculator(df,headers,nominal_attribute_no,label_attribute_no):
    # This varieble will save the all possible differences and will be the output
    indexed_sum_sqrd_difference=[]

    # This variable will save the values of each individual attributes as list of list
    indexed_elements=[]
    for index in nominal_attribute_no:
        #Save the differences for an attribute
        sum_sqrd_difference=[]

        #Calculate the output class for each attribute, this is an array of list with every list
        #containing a nominal attribute value and corrosponding output label; This data structure will separete the
        # target attribute and the corrosponding output label from the whole dataset to calculate frequency
        hvdm_check_levels= np.array(df.iloc[:,[index,label_attribute_no]])

        #This will find total count for each attribute value
        category_count=np.array(df.iloc[:,[index,label_attribute_no]].groupby(headers[index]).count().to_records().view(type=np.matrix))
        #This will count total count of each output label
        outputs= np.array(df.iloc[:,[index,label_attribute_no]].groupby(headers[label_attribute_no]).count().to_records().view(type=np.matrix))

        output_classes=[]
        elements=[]

        #Find total values in an attribute
        for data in category_count[0]:
            elements.append(data[0])
        indexed_elements.append([index,elements])

        #Find total output classes
        for data in outputs[0]:
            output_classes.append(data[0])

        #Calculate the frequency of each attribute value with each output classes
        elements_frequencies=[]
        for element in elements:
            for item in output_classes:
                frequencies=[]
                count=0
                for data in hvdm_check_levels:
                    if data[0]==element and data[1]==item:
                       count=count+1
                #Find total attributes
                total = 0
                #find total number of elements
                for x in category_count[0]:
                    if element==x[0]:
                       total=x[1]
                probability=count/total
                #print(element,item,count,total)
                frequencies=[element,item,probability]
                elements_frequencies.append(frequencies)

        #Calculate the squared difference of the probability for each attribute value with other attribute values and
        #output classes
        diffrences=[]
        demo_element_frequencies=elements_frequencies
        for item1 in elements_frequencies:
            for item in demo_element_frequencies:
                if item1[0]!=item[0] and item1[1]==item[1]:
                    probability_diffrence=item1[2]-item[2]
                    probability_diffrence_sqr=probability_diffrence*probability_diffrence
                    sqr_diffrence=[item1[0],item[0],item1[1],probability_diffrence_sqr]
                    diffrences.append(sqr_diffrence)
        #print(diffrences)

        #Calculate the sum for the probability differences between the values of attribute
        sqrd_difference=[]
        for item1 in diffrences:
            sum=0
            for item in diffrences:
                if item1[0]==item[0] and item1[1]==item[1]:
                    sum=sum+item[3]
            sum_smaples=[item1[0],item1[1],sum]
            sqrd_difference.append(sum_smaples)

        #Remove the duplicate values
        for item in sqrd_difference:
            if item not in sum_sqrd_difference:
                sum_sqrd_difference.append(item)

        #Add attribute index with value. Now we have attribute index, values of attributs and the sum of their squared
        #differences for different label
        indexed_sum_sqrd_difference.append([index,sum_sqrd_difference])
    return indexed_sum_sqrd_difference, indexed_elements
