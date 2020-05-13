import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from  sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
import collections

#HVDM metric implimentation

#Preparing data
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

new_df = pd.DataFrame(data=pd.get_dummies(df, columns=["sex"]))

max_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].max()
min_value = new_df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].min()

std = df[["length", "diameter", "height", "whole_weight",
           "shucked_weight", "viscera_weight", "shell_weight"]].std()


X = np.array(df.drop(['rings'], 1))
y = np.array(df['rings'])
#X_resampled, y_resampled = SMOTE().fit_resample(X, y)
X_resampled, y_resampled = BorderlineSMOTE(kind='borderline-1').fit_resample(X, y)
#X_resampled, y_resampled = BorderlineSMOTE(kind='borderline-2').fit_resample(X, y)
#X_resampled, y_resampled = ADASYN().fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=0)

#Test indics will come from stratified cross validation
rskf = RepeatedStratifiedKFold(n_splits=2, n_repeats=2,
    random_state=36851234)

for train_index, test_index in rskf.split(X_resampled, y_resampled):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X_resampled[train_index], X_resampled[test_index]
    #print("X_test index:",test_index)
    y_train, y_test = y_resampled[train_index], y_resampled[test_index]
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    #accuracy = clf.score(X_test, y_test)

    accuracy = clf.score(X_test, y_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print(tn, fp, fn, tp)

