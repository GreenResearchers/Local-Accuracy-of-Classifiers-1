import numpy as np
import fuzzyMembershipCalculator as f
import os


def subCategoryAndFuzzyMembershipFinder(distances,majority_label,minority_label,k,X,y):

    minority_index_array = np.where(y==minority_label)
    minority_index=minority_index_array[0].tolist()

    safe_list=[]
    boarderline_list=[]
    rare_list=[]
    outlier_list=[]


    for index in minority_index:

        distance = distances[index]
        sorted_k_distances=np.argsort(distance)[0:k+1]
        same_index = np.where(sorted_k_distances==index)
        sorted_k_distances = np.delete(sorted_k_distances,same_index,0)

        neighbour_weights = []

        for item in sorted_k_distances:
            neighbour_weights.append(distance[item])

        minority_count = 0
        majority_count = 0

        for sample in sorted_k_distances:
            if (y[sample] ==majority_label):
                majority_count += 1
            else:
                minority_count += 1

        minority_probability=minority_count/k
         # catagorize the samples
        if (minority_count>=9):
             # Append the safe and predict data to list
            membership=f.fuzzyMembership(sorted_k_distances,neighbour_weights,y,minority_label,k)
            safe_list.append(membership)

        elif (minority_count==7 and majority_count==8)or (minority_count==8 and majority_count==7):
             # Append the boarderline and predict data to list
            membership=f.fuzzyMembership(sorted_k_distances,neighbour_weights,y,minority_label,k)
            #print("Indexes:",sorted_k_distances,"\nWeights:",neighbour_weights,"\nMembership",membership)
            #for i in sorted_k_distances:
            #    print(y[i])
            boarderline_list.append(membership)

        elif (minority_count<=6 and minority_count>0):
             # Append the rare and predict data to list
            membership=f.fuzzyMembership(sorted_k_distances,neighbour_weights,y,minority_label,k)
            rare_list.append(membership)

        else:
             # Append the outlier and predict data to list#
            membership=f.fuzzyMembership(sorted_k_distances,neighbour_weights,y,minority_label,k)
            outlier_list.append(membership)

    #safe_count,safe_average,safe_maximum,safe_minimum=CountAverageMaxMin(safe_list)
    #safe=[]
    #safe.append(safe_count)
    #safe.append(safe_average)
    #safe.append(safe_maximum)
    #safe.append(safe_minimum)

    #borderline_count,borderlin_average,borderline_maximum,borderlin_minimum=CountAverageMaxMin(boarderline_list)
    #borderline=[]
    #borderline.append(borderline_count)
    #borderline.append(borderlin_average)
    #borderline.append(borderline_maximum)
    #borderline.append(borderlin_minimum)

    #rare_count,rare_average,rare_maximum,rare_minimum=CountAverageMaxMin(rare_list)
    #rare=[]
    #rare.append(rare_count)
    #rare.append(rare_average)
    #rare.append(rare_maximum)
    #rare.append(rare_minimum)

    #outlier_count,outlier_average,outlier_maximum,outlier_minimum=CountAverageMaxMin(outlier_list)
    #outlier=[]
    #outlier.append(outlier_count)
    #outlier.append(outlier_average)
    #outlier.append(outlier_maximum)
    #outlier.append(outlier_minimum)

    return  safe_list,boarderline_list,rare_list,outlier_list

def plotGraph(list):

    return

def CountAverageMaxMin(list):
    count=0
    total=0
    maximum=0
    if (len(list)!=0):
        minimum=list[0]
        for item in list:
            count=count+1
            if(item>maximum):
                maximum=item
            if(item<minimum):
                minimum=item
            total=total+item
        average=total/count
        return count,average,maximum,minimum
    else:
        return 0,0,0,0

def write(safe,borderline,rare,outlier,str):
    #write answer to file
    filepath = os.path.join('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/MembershipCalculation/analysis_membership3' 'filename3')
    if not os.path.exists('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/MembershipCalculation/analysis_membership3'):
        os.makedirs('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/MembershipCalculation/analysis_membership3')
    f = open(filepath, "a+")
    f.write(str)
    f.write("Category:[Count, Average, Maximum, Minimum]\n")
    f.write("Safe:%s\n" % safe)
    f.write("Borderline:%s\n" % borderline)
    f.write("Rare:%s\n" % rare)
    f.write("Outlier:%s\n" % outlier)
    f.write("\n")
    f.close()

    return

def write_separetely(safe,borderline,rare,outlier,path):
    #write answer to file
    str=path+'safe.txt'
    filepath_safe = os.path.join(str)
    f = open(filepath_safe, "a+")
    for item in safe:
        f.write("%s" %item)
        f.write("\n")
    f.close()

    str=path+'borderline.txt'
    filepath_borderline = os.path.join(str)
    f = open(filepath_borderline, "a+")
    for item in borderline:
        f.write("%s" %item)
        f.write("\n")
    f.close()

    str=path+'rare.txt'
    filepath_rare = os.path.join(str)
    f = open(filepath_rare, "a+")
    for item in rare:
        f.write("%s" %item)
        f.write("\n")
    f.close()

    str=path+'outlier.txt'
    filepath_outlier = os.path.join(str)
    f = open(filepath_outlier, "a+")
    for item in outlier:
        f.write("%s" %item)
        f.write("\n")
    f.close()
    return
