import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from  sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
import collections
import math
import random

#HVDM metric implimentation

#Preparing data
headers = ["wife_age", "wife_edu", "husband_edu", "no_child", "wife_reli","wife_work","husband_occu",
           "living_index","media_exxpo","class"]

df = pd.read_csv("cmc.data", header=None, names=headers, na_values="?")


replace_lebels = {"class":     {1: 0, 3: 0, 2:4}}
df.replace(replace_lebels, inplace=True)

std = df[["wife_age","no_child"]].std()
std= 4 * std.values

nominal_attribute_no=[1,2,4,5,6,7,8]
numeric_attribute_no=[0,3]
label_attribute_no=9
minority_label=4
majority_label=0
K=[5,7,9,11,13,15,17,19]

# # std= 4 * std.values
##Elements for HVDM calculation
indexed_sum_sqrd_difference=[]
indexed_elements=[]
for index in nominal_attribute_no:
    sum_sqrd_difference=[]

    #Calculate the output class for each attribute, this is an array of list with every list
    #containing a nominal attribute value and corrosponding output label; This data structure will separete the
    # target attribute and the corrosponding output label to calculate frequency
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


def SO(X,y, l):
    #Find the minority class by counting the data
    #count = collections.Counter(y)
    minority_index = []
    X_resampled=X
    y_resampled=y
    minority_index = np.where(y==l)
    minority_index = minority_index[0].tolist()
    safe=0
    boarderline=0
    rare=0
    outlier=0

    for a in minority_index:
        #knn = NearestNeighbors(n_neighbors=6)
        #knn = NearestNeighbors(n_neighbors=6, algorithm='ball_tree', metric='pyfunc', metric_params={"func":HVDM})
        distances=[]
        for b in X:
            #distances.append(HVDM(a,b))
            z=0
            c=0
            sqr_std_dist_col_nominal=0
            for attribute in numeric_attribute_no:
                normalized_diff = (X[a][attribute] - b[attribute]) / (4*std[c])
                normalized_diff=normalized_diff*normalized_diff
                z=normalized_diff+z
                c=c+1

            for attribute in nominal_attribute_no:
                sqr_std_dist_col=0
                if X[a][attribute] == b[attribute]:
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
            distances.append(math.sqrt(z + sqr_std_dist_col_nominal))

        new_neighbours=np.argsort(distances)[0:6]
        #new_neighbours_distances=np.sort(distances)[0:6]

        same_index = np.where(new_neighbours==a)
        new_neighbours = np.delete(new_neighbours,same_index,0)
        #new_neighbours_distances = np.delete(new_neighbours_distances,same_index,0)
        minority_count = 0
        majority_count = 0

        for sample in new_neighbours:
            if (y[sample] !=l):
                minority_count += 1

            else:
                majority_count += 1



        # catagorize the samples
        if (minority_count == 5 and majority_count == 0) or (minority_count == 4 and majority_count == 1):
            # Append the safe and predict data to list
            safe = safe + 1

        elif (minority_count == 2 and majority_count == 3) or (minority_count == 3 and majority_count == 2):
             #Find the nearest majority neighbour
            target = 0
            for sample in new_neighbours:
                if y[sample]!=l:
                    continue
                else:
                    target = sample
                    break
            diff = np.absolute(X[a]-X[target])
            co = 0
            while co < 9:
                adding_value= diff* random.uniform(0.001, 0.5)
                new_sample = X[a] + adding_value
                X_resampled=np.append(X_resampled,[new_sample],axis=0)
                y_resampled=np.append(y_resampled,l)
                co=co+1

        elif minority_count == 1 and majority_count == 4:
            # Append the rare and predict data to list
            target = 0
            for sample in new_neighbours:
                if y[sample]!=l:
                    continue
                else:
                    target = sample
                    break
            diff = np.absolute(X[a]-X[target])
            co = 0
            while co < 12:
                adding_value= diff* random.uniform(0.001, 0.5)
                new_sample = X[a] + adding_value
                X_resampled=np.append(X_resampled,[new_sample],axis=0)
                y_resampled=np.append(y_resampled,l)
                co=co+1


        else:
            # Append the outlier and predict data to list
            target = 0
            for sample in new_neighbours:
                if y[sample]!=l:
                    continue
                else:
                    target = sample
                    break

            diff = np.absolute(X[a]-X[target])
            co = 0
            while co < 13:
                adding_value= diff* random.uniform(0.001, 0.5)
                new_sample = X[a] + adding_value
                X_resampled=np.append(X_resampled,[new_sample],axis=0)
                y_resampled=np.append(y_resampled,l)
                co=co+1


    return X_resampled, y_resampled

X = np.array(df.drop(['class'], 1))
y = np.array(df['class'])
X_resampled, y_resampled = SO(X, y, minority_label)
#X_resampled, y_resampled = SMOTE().fit_resample(X, y)
#X_resampled, y_resampled = BorderlineSMOTE(kind='borderline-1').fit_resample(X, y)
#X_resampled, y_resampled = BorderlineSMOTE(kind='borderline-2').fit_resample(X, y)
#X_resampled, y_resampled = ADASYN().fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=0)

#Test indics will come from stratified cross validation
rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=5,
    random_state=36851234)
ttn=0
tfp=0
tfn=0
ttp=0
tn=0
fp=0
fn=0
tp=0
count =0
for train_index, test_index in rskf.split(X_resampled, y_resampled):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X_resampled[train_index], X_resampled[test_index]
    #print("X_test index:",test_index)
    y_train, y_test = y_resampled[train_index], y_resampled[test_index]
    #clf = neighbors.KNeighborsClassifier()
    clf= DecisionTreeClassifier(random_state=0)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    #accuracy = clf.score(X_test, y_test)

    accuracy = clf.score(X_test, y_test)
    ctn, cfp, cfn, ctp = confusion_matrix(y_test, y_pred).ravel()
    ttn=ttn+ctn
    tfp=tfp+cfp
    tfn=tfn+cfn
    ttp=ttp+ctp
    tn=ttn/50
    fp=tfp/50
    fn=tfn/50
    tp=ttp/50
    count =count+1


print("Count:",count)
print("TN:",tn,"FP:", fp,"FN:", fn,"TP:", tp)
acc=(tp+tn)/(tp+fn+fp+tn)
print("Accuracy:",acc)
tpr=tp/(tp+fn)
print("TPR:",tpr)
tnr=tn/(fp+tn)
print("TNR:",tnr)
fpr=fp/(fp+tn)
print("FPR:",fpr)
fnr=fn/(tp+fn)
print("FNR:",fnr)
GM=math.sqrt(tpr*tnr)
print("GM",GM)
AUC=(1+tpr-fpr)/2
print("AUC:",AUC)
PPV=tp/(tp+fp)
b=1
fm=(((1+(b*b))*(PPV*tpr))/(((b*b)*PPV)+tpr))
print("FM:",fm)
