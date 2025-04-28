import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import csv

# Get the training data
df = pd.read_csv("C:\\Users\\wzhyt\\Downloads\\dont_delete\\AIPRACWINES\\wine-label-decoder\\dataset\\NY_OR_WA_wines.csv")

# Assigning category value to integer
region = set(df['region'])
grape = set(df['grape'])
result = set(zip(df['grape_law'], df['region_law'], df['vintage_law']))
region_mp = {value : idx for idx, value in enumerate(region)}
grape_mp = {value : idx for idx, value in enumerate(grape)}
result_mp = {tup : str(idx) for idx, tup in enumerate(result)}
df['region'] = df['region'].map(region_mp)
df['grape'] = df['grape'].map(grape_mp)
df['result'] = df.apply(lambda row: result_mp.get((row['grape_law'], row['region_law'], row['vintage_law']), 'None'), axis=1)

# Removing useless columns
df = df.drop(df.columns[7], axis = 1)
df = df.drop(df.columns[6], axis = 1)
df = df.drop(df.columns[5], axis = 1)
df = df.drop(df.columns[4], axis = 1)
df = df.drop(df.columns[3], axis = 1)
df = df.drop(df.columns[0], axis = 1)

# print(df.head())

# Decision Tree
X = df[['grape', 'region']]
Y = df[['result']]

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, Y)


# Testing decision tree model
# TODO
X_new = pd.DataFrame([[2, 21]], columns=['grape', 'region'])
print(dtree.predict(X_new))

