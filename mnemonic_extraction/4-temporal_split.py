import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split



df = pd.read_csv("ELF_Dataset_Timestamps.csv")

df["date_of_day"] = df.apply(lambda x: datetime.strptime(x["date_of_day"], '%Y-%m-%d'), axis=1)

df = df.sort_values("date_of_day", ascending=True)
df.to_csv("ELF_Dataset_Timestamps.csv")

X = np.array(df["sha256_hash"])
Y = np.array(df["label"])
T = np.array(df["date_of_day"])

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.75, shuffle=False, stratify=None)

print(Y_train[Y_train == 0].size, Y_train[Y_train == 1].size)
print(Y_test[Y_test == 0].size, Y_test[Y_test == 1].size)

print(all(np.hstack((X_train, X_test)) == X))

with open("DataSplit.pkl", "wb") as fwbPkl:
    pickle.dump([X_train, X_test, Y_train, Y_test], fwbPkl)
