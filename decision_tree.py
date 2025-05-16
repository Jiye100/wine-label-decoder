import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import csv
import sys

# Get the training data
ny_or_wa_df = pd.read_csv(r'dataset/NY_OR_WA_wines.csv')
ca_df = pd.read_csv(r'dataset/CA_wines.csv')
cl_arg_za_df = pd.read_csv(r'dataset/CL_ARG_ZA_wines.csv')
nz_au_df = pd.read_csv(r'dataset/NZ_AU_wines.csv')

df = pd.concat([ny_or_wa_df, ca_df, cl_arg_za_df, nz_au_df], ignore_index=True)


# Assigning category value to integer
region = set(df['region'])
grape = set(df['grape'])
country = set(df['country'])
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

#print(df.head())
# Removing useless columns
df = df.drop(df.columns[6], axis = 1)
df = df.drop(df.columns[5], axis = 1)
df = df.drop(df.columns[4], axis = 1)
df = df.drop(df.columns[3], axis = 1)

# Decision Tree
X = df[['grape', 'region', 'country', 'designation']]
Y = df[['result']]

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, Y)


# Testing decision tree model
# TODO
#X_new = pd.DataFrame([[2, 21, 1, 2]], columns=['grape', 'region', 'country', 'designation'])
#print(dtree.predict(X_new))
'''
def predict_law(df):
    df['region'] = df['region'].map(region_mp)
    df['grape'] = df['grape'].map(grape_mp)
    df['country'] = df['country'].map(country_mp)
    df['designation'] = df['designation'].map(designation_mp)

    pred = dtree.predict(df)

    print("prediction done")

    return idx2result[pred[0]]

'''
def predict_law(df):
    """
    Predicts the grape, region, and vintage law based on the attributes.
    
    Arguments:
    df (DataFrame): A DataFrame with columns ['grape', 'region', 'country', 'designation']
    
    Returns:
    tuple: (grape_law, region_law, vintage_law)
    """
    # --- Check if the input is a DataFrame ---
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a DataFrame with columns: ['grape', 'region', 'country', 'designation']")
    
    # --- Map the values to their indices ---
    df['grape'] = df['grape'].map(grape_mp)
    df['region'] = df['region'].map(region_mp)
    df['country'] = df['country'].map(country_mp)
    df['designation'] = df['designation'].map(designation_mp)

    # --- If mapping failed for any column, raise an error ---
    if df.isnull().values.any():
        raise ValueError("One or more values not found in mappings.")

    # --- Make the prediction ---
    pred = dtree.predict(df)

    # --- Map back to the result tuple ---
    if pred[0] in idx2result:
        #print(f"Prediction for input: {idx2result[pred[0]]}")
        return idx2result[pred[0]]
    else:
        raise ValueError(f"Prediction resulted in an unknown label: {pred[0]}")
