import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

# Load the data
ny_or_wa_df = pd.read_csv(r'dataset/NY_OR_WA_wines.csv')
ca_df = pd.read_csv(r'dataset/CA_wines.csv')

# Combine datasets
df = pd.concat([ny_or_wa_df, ca_df], ignore_index=True)

# Mapping categorical values to integers
region = set(df['region'])
grape = set(df['grape'])
country = set(df['country'])
designation = set(df['designation'])
result = set(zip(df['grape_law'], df['region_law'], df['vintage_law']))

region_mp = {value: idx for idx, value in enumerate(region)}
grape_mp = {value: idx for idx, value in enumerate(grape)}
country_mp = {value: idx for idx, value in enumerate(country)}
designation_mp = {value: idx for idx, value in enumerate(designation)}
result_mp = {tup: str(idx) for idx, tup in enumerate(result)}
idx2result = {str(idx): tup for tup, idx in result_mp.items()}

# Map categorical columns
df['region'] = df['region'].map(region_mp)
df['grape'] = df['grape'].map(grape_mp)
df['country'] = df['country'].map(country_mp)
df['designation'] = df['designation'].map(designation_mp)
df['result'] = df.apply(lambda row: result_mp.get((row['grape_law'], row['region_law'], row['vintage_law']), 'None'), axis=1)

# Drop unnecessary columns
df = df.drop(['grape_law', 'region_law', 'vintage_law', 'estate', 'vintage'], axis=1)

# Define features and target
X = df[['grape', 'region', 'country', 'designation']]
Y = df['result'].astype(str)

# Initialize the Decision Tree model
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

# --- Train on Full Data and Save the Model ---
print("\nTraining final model on full dataset...")
dtree.fit(X, Y)
joblib.dump(dtree, 'decision_tree_model.pkl')
print("Model saved as 'decision_tree_model.pkl'")
