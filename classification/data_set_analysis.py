from numpy import bitwise_not
from pandas import DataFrame, read_feather
from sklearn.cluster import KMeans

data_set = read_feather("data.feather")

features = data_set.columns.to_list()
features.remove("malicious")
features.remove("family")
features.remove("architecture")
features.remove("abi")

x = data_set[features]
y = data_set["malicious"]

d = DataFrame()
malicious_means = []
malicious_stds = []
benign_means = []
benign_stds = []
separabilities = []
for feature in features:
    malicious = data_set[feature][y]
    benign = data_set[feature][bitwise_not(y)]
    malicious_mean = malicious.mean()
    malicious_std = malicious.std()

    benign_mean = benign.mean()
    benign_std = benign.std()

    model = KMeans(n_clusters=2)
    model.fit(x[feature].to_numpy().reshape(-1, 1))
    yy = model.labels_
    separability = max((y == yy).sum(), (y != yy).sum()) / len(y) * 100

    malicious_means.append(malicious_mean)
    malicious_stds.append(malicious_std)

    benign_means.append(benign_mean)
    benign_stds.append(benign_std)

    separabilities.append(separability)

    print(feature, separability)

# f["accuracy"] = v
d["feature"] = features
d["malicious_mean"] = malicious_means
d["malicious_std"] = malicious_stds
d["benign_mean"] = benign_means
d["benign_std"] = benign_stds
d["separability"] = separabilities
d.sort_values(by="separability", ascending=False, inplace=True)
d.to_csv("dataset_analysis.csv", index=False)
