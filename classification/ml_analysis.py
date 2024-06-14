from warnings import catch_warnings

from numpy import bitwise_not
from pandas import DataFrame, read_feather, read_csv
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier

train_set = read_feather("feather/train.feather")
test_set = read_feather("feather/test.feather")

features = read_csv("dataset_analysis.csv")

train_x = train_set[features["feature"]]
train_y = train_set["malicious"]
test_x = test_set[features["feature"]]
test_y = test_set["malicious"]

classifiers = [LogisticRegression(), LinearSVC(), DecisionTreeClassifier()]
m = 20

with catch_warnings(action="ignore"):
    for classifier in classifiers:
        f = []
        print(classifier)
        for _, row in features.iterrows():
            feature = row["feature"]
            separability = row["separability"]
            if len(f) >= m:
                break
            f.append(feature)
            classifier.fit(train_x[f], train_y)
            yy = classifier.predict(test_x[f])
            score = balanced_accuracy_score(test_y, yy)
            print(f"\t({len(f)}, {score * 100})")

print("")
with catch_warnings(action="ignore"):
    for classifier in classifiers:
        print(classifier)
        f = []
        for _, row in features.iloc[::-1].iterrows():
            feature = row["feature"]
            separability = row["separability"]
            if len(f) >= m:
                break
            f.append(feature)
            classifier.fit(train_x[f], train_y)
            yy = classifier.predict(test_x[f])
            score = balanced_accuracy_score(test_y, yy)
            print(f"\t({len(f)}, {score * 100})")
