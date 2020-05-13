import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from  sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import neighbors
from sklearn.metrics import accuracy_score
import math
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import MinMaxScaler

headers = ["sex", "length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight", "rings"]

df = pd.read_csv("abalone.data", header=None, names=headers, na_values="?")

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
print(df['rings'])
new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["sex"]))

max_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].max()
min_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].min()

std = df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].std()

hvdm_check_levels= np.array(df.drop(["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"], 1))
total_male= 0
total_female= 0
total_infant= 0
total_male_majority = 0
total_male_minority= 0
total_female_majority= 0
total_female_minority= 0
total_infant_majority= 0
total_infant_minority= 0

for item in hvdm_check_levels:
    if item[0] == 0:
        total_male = total_male + 1
        if item[1] <= 4 or item[1]>= 16:
            total_male_minority = total_male_minority + 1
        else:
            total_male_majority = total_male_majority + 1

    elif item[0] == 1:
        total_female = total_female + 1
        if item[1] <= 4 or item[1]>= 16:
            total_female_minority = total_female_minority + 1
        else:
            total_female_majority = total_female_majority + 1

    elif item[0] == 2:
        total_infant = total_infant + 1
        if item[1] <= 4 or item[1]>= 16:
            total_infant_minority = total_infant_minority + 1
        else:
            total_infant_majority = total_infant_majority + 1

probable_sex_male_majority=total_male_majority/total_male
probable_sex_male_minority=total_male_minority/total_male
probable_sex_female_majority = total_female_majority / total_female
probable_sex_female_minority = total_female_minority / total_female
probable_sex_infant_majority = total_infant_majority / total_infant
probable_sex_infant_minority = total_infant_minority / total_infant

DifferenceMaleFemaleMajority = probable_sex_male_majority - probable_sex_female_majority
SqrdDifferenceMaleFemaleMajority= DifferenceMaleFemaleMajority * DifferenceMaleFemaleMajority

DifferenceMaleFemaleMinority = probable_sex_male_minority - probable_sex_female_minority
SqrdDifferenceMaleFemaleMinority= DifferenceMaleFemaleMinority * DifferenceMaleFemaleMinority

DifferenceMaleInfantMajority = probable_sex_male_majority - probable_sex_infant_majority
SqrdDifferenceMaleInfantMajority= DifferenceMaleInfantMajority * DifferenceMaleInfantMajority

DifferenceMaleInfantMinority = probable_sex_male_minority - probable_sex_infant_minority
SqrdDifferenceMaleInfantMinority= DifferenceMaleInfantMinority * DifferenceMaleInfantMinority

DifferenceFemaleInfantMajority = probable_sex_female_majority - probable_sex_infant_majority
SqrdDifferenceFemaleInfantMajority= DifferenceFemaleInfantMajority * DifferenceFemaleInfantMajority

DifferenceFemaleInfantMinority = probable_sex_female_minority - probable_sex_infant_minority
SqrdDifferenceFemaleInfantMinority= DifferenceFemaleInfantMinority * DifferenceFemaleInfantMinority

SumSqrdDifferenceMaleFemale = SqrdDifferenceMaleFemaleMajority + SqrdDifferenceMaleFemaleMinority
SumSqrdDifferenceMaleInfant = SqrdDifferenceMaleInfantMajority + SqrdDifferenceMaleInfantMinority
SumSqrdDifferenceFemaleInfant = SqrdDifferenceFemaleInfantMajority + SqrdDifferenceFemaleInfantMinority

def HVDM(a, b):
    sqr_std_dist_col0 = 0

    if a[0] == b[0]:
        sqr_std_dist_col0 = 0

    elif (a[0] == 0 and b[0] == 1) or (a[0] == 1 and b[0] == 0):
        sqr_std_dist_col0 = SumSqrdDifferenceMaleFemale

    elif (a[0] == 0 and b[0] == 2) or (a[0] == 2 and b[0] == 0):
        sqr_std_dist_col0 = SumSqrdDifferenceMaleInfant

    elif (a[0] == 1 and b[0] == 2) or (a[0] == 2 and b[0] == 1):
        sqr_std_dist_col0 = SumSqrdDifferenceFemaleInfant

    z = (a[1:8] - b[1:8]) / std[0:7]
    total_distance = math.sqrt((z * z).sum() + sqr_std_dist_col0)

    return total_distance



range= max_value-min_value
new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]]= \
    ((new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]]-min_value)/std)

iteration_total_data = []
iteration_majority_data = []
iteration_minority_data= []
iteration_safe_data =[]
iteration_boarderline_data =[]
iteration_rare_data= []
iteration_outlier_data=[]

iteration_total_accuracy = []
iteration_majority_accuracy  = []
iteration_minority_accuracy = []
iteration_safe_accuracy  =[]
iteration_boarderline_accuracy  =[]
iteration_rare_accuracy = []
iteration_outlier_accuracy =[]

X = np.array(new_df.drop(['rings'], 1))
y = np.array(new_df['rings'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=36851234)
splits=2
repeats=5
length=splits*repeats

rskf = RepeatedStratifiedKFold(n_splits=splits, n_repeats=repeats,
    random_state=36851234)
for train_index, test_index in rskf.split(X, y):
    print("\n\nNew iteration:\n\n")
    #Separete train and test indics for X and y
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    #initialize the taret classifier and train it
    #clf = neighbors.KNeighborsClassifier(n_neighbors=3)
    #clf=SVC()
    #clf=GaussianProcessClassifier(1.0 * RBF(1.0))
    clf=DecisionTreeClassifier(max_depth=5)
    #clf=MLPClassifier(alpha=1)
    clf.fit(X_train, y_train)

    #Store the predicted values
    y_pred = clf.predict(X_test)

    #Calculate global accuracy
    accuracy = accuracy_score(y_test, y_pred)
    #accuracy = clf.score(X_test, y_test)
    accuracy = clf.score(X_test, y_test)

    minority_y_test_index = []

    minority_y_test_index1 = np.where(y_test <=4)
    minority_y_test_index2 = np.where(y_test >=16)
    total_indexes = np.where(y_test>=0)
    minority_y_test_index1_list1 = minority_y_test_index1[0].tolist()
    minority_y_test_index2_list2 = minority_y_test_index2[0].tolist()


    minority_y_test_index= minority_y_test_index1_list1 + minority_y_test_index2_list2
    y_pred_minority = []
    y_test_minority = []

    majority_test_index = total_indexes

    for item in minority_y_test_index:
        y_test_minority.append(y_test[item])
        y_pred_minority.append(y_pred[item])

    majority_test_index=np.delete(majority_test_index,minority_y_test_index)

    accuracy_minority = accuracy_score(y_test_minority, y_pred_minority)

    y_pred_majority = []
    y_test_majority = []

    for item in majority_test_index:
        y_test_majority.append(y_test[item])
        y_pred_majority.append(y_pred[item])
        #print(y_test[item])
    accuracy_majority = accuracy_score(y_test_majority, y_pred_majority)

    print("Total Data:",len(test_index))
    iteration_total_data.append(len(test_index))
    print("Majority data:", len(majority_test_index))
    iteration_majority_data.append(len(majority_test_index))
    print("Total Minority Data:",len(minority_y_test_index))
    iteration_minority_data.append(len(minority_y_test_index))
    print("Global accuracy:", accuracy)
    iteration_total_accuracy.append(accuracy)
    print("Global Minority accuracy:",accuracy_minority)
    iteration_minority_accuracy.append(accuracy_minority)
    print("Global Majority accuracy:",accuracy_majority)
    iteration_majority_accuracy.append(accuracy_majority)
    minority_index_main_data = []

    for index in minority_y_test_index:
        minority_index_main_data.append([test_index[index], index])

    np.asarray(minority_index_main_data)
    #Variebles to save results about minority data
    y_test_safe = []
    np.asarray(y_test_safe)
    y_pred_safe = []
    np.asarray(y_pred_safe)
    safe=0

    y_test_boarderline = []
    np.asarray(y_test_boarderline)
    y_pred_boarderline = []
    np.asarray(y_pred_boarderline)
    boarderline=0

    y_test_rare = []
    np.asarray(y_test_rare)
    y_pred_rare = []
    np.asarray(y_pred_rare)
    rare=0

    y_test_outlier = []
    np.asarray(y_test_outlier)
    y_pred_outlier = []
    np.asarray(y_pred_outlier)
    outlier=0

    #Finding five neighbourhood of the minority data from test samples
    for index in minority_index_main_data:
        knn = NearestNeighbors(n_neighbors=6, algorithm='ball_tree', metric='euclidean')
        #knn =  NearestNeighbors(n_neighbors=6, algorithm='ball_tree', metric='pyfunc', metric_params={"func":HVDM})
        knn.fit(X)
        neighbours = (knn.kneighbors([X[index[0]]], return_distance=False))
        new_neighbours = [item for sub_neighbours in neighbours for item in sub_neighbours]

        #remove self index or extra index from the list
        if index[0] in new_neighbours:
            new_neighbours.remove(index[0])
        else:
            del new_neighbours[5]

        #separete the minority and majority samples from the samples
        minority_count = 0
        majority_count = 0
        for sample in new_neighbours:
            #print("Data lebel:",y[index])
            if (y[sample] > 4 and y[sample]<16):
                #print("Minority Incremented")
                majority_count += 1
            else:
                #print("Maority Incremented")
                minority_count += 1
        #print("Minority count:", minority_count, "Majority_count", majority_count)

        #catagorize the samples

        if (minority_count == 5 and majority_count == 0)or(minority_count == 4 and majority_count == 1):
            #Append the safe and predict data to list
            y_test_safe.append(y_test[index[1]])
            y_pred_safe.append(y_pred[index[1]])
            safe=safe+1

        elif(minority_count == 2 and majority_count == 3) or (minority_count == 3 and majority_count == 2):

            #Append the boarderline and predict data to list
            y_test_boarderline.append(y_test[index[1]])
            y_pred_boarderline.append(y_pred[index[1]])
            boarderline=boarderline+1

        elif minority_count == 1 and majority_count == 4:

            #Append the rare and predict data to list
            y_test_rare.append(y_test[index[1]])
            y_pred_rare.append(y_pred[index[1]])
            rare=rare+1

        else:

            #Append the outlier and predict data to list
            y_test_outlier.append(y_test[index[1]])
            y_pred_outlier.append(y_pred[index[1]])
            outlier=outlier+1

    # Find the accuracy for safe samples
    accuracy_safe = accuracy_score(y_test_safe, y_pred_safe)
    print("Safe:", safe)
    iteration_safe_data.append(safe)
    print("Accuracy for Safe:",accuracy_safe)
    iteration_safe_accuracy.append(accuracy_safe)

    # Find the accuracy for boarderline samples
    accuracy_boarderline = accuracy_score(y_test_boarderline, y_pred_boarderline)
    print("Boarderline:", boarderline)
    print("Accuracy for Boarderline:",accuracy_boarderline)
    iteration_boarderline_data.append(boarderline)
    iteration_boarderline_accuracy.append(accuracy_boarderline)

    # Find the accuracy for rare samples
    accuracy_rare = accuracy_score(y_test_rare, y_pred_rare)
    print("Rare",rare)
    print("Accuracy for Rare:",accuracy_rare)
    iteration_rare_data.append(rare)
    iteration_rare_accuracy.append(accuracy_rare)

    # Find the accuracy for outlier samples
    accuracy_outlier = accuracy_score(y_test_outlier, y_pred_outlier)
    print("Outlier",outlier)
    print("Accuracy for outlier:",accuracy_outlier)
    iteration_outlier_data.append(outlier)
    iteration_outlier_accuracy.append(accuracy_outlier)

print("\n\nFinal Average\n\n")

avg_total_data = sum(iteration_total_data)/length
avg_majority_data = sum(iteration_majority_data)/length
avg_minority_data= sum(iteration_minority_data)/length
avg_safe_data =sum(iteration_safe_data)/length
avg_boarderline_data =sum(iteration_boarderline_data)/length
avg_rare_data= sum(iteration_rare_data)/length
avg_outlier_data=sum(iteration_outlier_data)/length

avg_total_accuracy = sum(iteration_total_accuracy)/length
avg_majority_accuracy  = sum(iteration_majority_accuracy)/length
avg_minority_accuracy = sum(iteration_minority_accuracy)/length
avg_safe_accuracy  =sum(iteration_safe_accuracy)/length
avg_boarderline_accuracy  =sum(iteration_boarderline_accuracy)/length
avg_rare_accuracy = sum(iteration_rare_accuracy)/length
avg_outlier_accuracy = sum(iteration_outlier_accuracy)/length

print("Average Total Data:",avg_total_data)
print("Average Total Accuracy",avg_total_accuracy)
print("Average Majority Data",avg_majority_data)
print("Average Majority Accuracy",avg_majority_accuracy)
print("Average Minority Data",avg_minority_data)
print("Average Minority Accuracy",avg_minority_accuracy)
print("Average Safe Data",avg_safe_data)
print("Average Safe Accuracy",avg_safe_accuracy)
print("Average Boaderline Data", avg_boarderline_data)
print("Average Boarderline Accuracy", avg_boarderline_accuracy)
print("Average Rare Data",avg_rare_data)
print("Average Rare Accuracy",avg_rare_accuracy)
print("Average Outlier Data",avg_outlier_data)
print("Average Outlier Accuracy",avg_outlier_accuracy)