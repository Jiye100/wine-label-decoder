import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import csv
import sys
import joblib
import json

Config = json.load(open('./Config.json'))


# Get the training data
ny_or_wa_df = pd.read_csv(r'dataset/NY_OR_WA_wines.csv')
ca_df = pd.read_csv(r'dataset/CA_wines.csv')
cl_arg_za_df = pd.read_csv(r'dataset/CL_ARG_ZA_wines.csv')
nz_au_df = pd.read_csv(r'dataset/NZ_AU_wines.csv')

df = pd.concat([ny_or_wa_df, ca_df, cl_arg_za_df, nz_au_df], ignore_index=True)


# Assigning category value to integer
region = set(df['region'])
for reg in Config["regions"]:
    region.add(reg)
grape = set(df['grape'])
for grap in Config["grape_variety"]:
    grape.add(grap)
country = set(df['country'])
for c in Config["country"]:
    country.add(c)
designation = set(df['designation'])
result = set(zip(df['grape_law'], df['region_law'], df['vintage_law']))

region_mp = {value : idx for idx, value in enumerate(region)}
grape_mp = {value : idx for idx, value in enumerate(grape)}
country_mp = {value : idx for idx, value in enumerate(country)}
designation_mp = {value : idx for idx, value in enumerate(designation)}
result_mp = {tup : str(idx) for idx, tup in enumerate(result)}

idx2result = {str(idx): tup for tup, idx in result_mp.items()}

df['region'] = df['region'].map(region_mp)
df['grape'] = df['grape'].map(grape_mp)
df['country'] = df['country'].map(country_mp)
df['designation'] = df['designation'].map(designation_mp)
df['result'] = df.apply(lambda row: result_mp.get((row['grape_law'], row['region_law'], row['vintage_law']), 'None'), axis=1)

# print(df.head())
# Removing useless columns
df = df.drop(df.columns[6], axis = 1)
df = df.drop(df.columns[5], axis = 1)
df = df.drop(df.columns[4], axis = 1)
df = df.drop(df.columns[3], axis = 1)

# Decision Tree
X = df[['grape', 'region', 'country', 'designation']]
Y = df[['result']]

def decision_tree_train():
    dtree = DecisionTreeClassifier()

    # --- Cross-Validation (5-fold) ---
    print("Performing 5-fold Cross Validation...")
    scores = cross_val_score(dtree, X, Y, cv=5, scoring='accuracy')

    # Display results
    print("\nCross-Validation Scores:")
    for i, score in enumerate(scores):
        print(f"Fold {i + 1}: {score * 100:.2f}%")

    print(f"\nAverage Accuracy: {np.mean(scores) * 100:.2f}%")
    print(f"Standard Deviation: {np.std(scores) * 100:.2f}%")

    dtree = dtree.fit(X, Y)
    joblib.dump(dtree, './models/decision_tree_model.pkl')

def predict_law(input_df):
    """
    Predicts the grape, region, and vintage law based on the attributes.
    
    Arguments:
    df (DataFrame): A DataFrame with columns ['grape', 'region', 'country', 'designation']
    
    Returns:
    tuple: (grape_law, region_law, vintage_law)
    """
    # --- Check if the input is a DataFrame ---
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("Input must be a DataFrame with columns: ['grape', 'region', 'country', 'designation']")
    
    # --- Map the values to their indices ---
    input_df['grape'] = input_df['grape'].map(grape_mp)
    input_df['region'] = input_df['region'].map(region_mp)
    input_df['country'] = input_df['country'].map(country_mp)
    input_df['designation'] = input_df['designation'].map(designation_mp)

    # --- If mapping failed for any column, raise an error ---
    if input_df.isnull().values.any():
        return (0, 0, 0)

    # --- Make the prediction ---
    model = joblib.load('models/decision_tree_model.pkl')
    pred = model.predict(input_df)

    # --- Map back to the result tuple ---
    if pred[0] in idx2result:
        return idx2result[pred[0]]
    else:
        return (0, 0, 0)
