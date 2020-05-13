import numpy as np
import os

def auc(distances,minority_label,majority_label,K,y):

    ##Elements for HVDM calculation
    AUC_all=[]
    for k in K:
        count =0
        TP=0
        TN=0
        FP=0
        FN=0
        for distance in distances:

            sorted_k_distances=np.argsort(distance)[0:k+1]
            same_index = np.where(sorted_k_distances==count)
            sorted_k_distances = np.delete(sorted_k_distances,same_index,0)
            minority_count = 0
            majority_count = 0

            for sample in sorted_k_distances:
                if (y[sample] ==majority_label):
                    majority_count += 1
                else:
                    minority_count += 1
            predicted_label=0
            true_label=y[count]
            if(majority_count>minority_count):
                predicted_label = majority_label
            else:
                predicted_label = minority_label
            if(true_label==minority_label and predicted_label==true_label):
                TP=TP+1
            elif (true_label==minority_label and predicted_label!=true_label):
                FN=FN+1
            elif (true_label==majority_label and predicted_label==true_label):
                TN=TN+1
            elif (true_label==majority_label and predicted_label!=true_label):
                FP=FP+1
            count = count + 1

        TP_rate=TP/(TP+FN)
        TN_rate=TN/(FP+TN)
        FP_rate=FP/(FP+TN)
        AUC=(1+TP_rate-FP_rate)/2
        data=[k,AUC,TP_rate,TN_rate]
        AUC_all.append(data)

    return AUC_all

def write(AUC_all,str):
    #write answer to file
    filepath = os.path.join('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/SelectionOfk/AUC/analysis_AUC' 'filename')
    if not os.path.exists('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/SelectionOfk/Gmean/analysis_AUC'):
        os.makedirs('C:/Users/Mahin/Google Drive/Workspace/Local Accuracy of Classifiers/Project/Fuzzy Membership/SelectionOfk/Gmean/analysis_AUC')
    f = open(filepath, "a+")
    f.write(str)
    for item in AUC_all:
        f.write("%s\n" % item)
    f.write("\n")
    f.close()

    return
