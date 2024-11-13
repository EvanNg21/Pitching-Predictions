# -*- coding: utf-8 -*-
"""Pitching.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sEx73iYu1L6U6ATbQqHVfOccVY4v8_Yw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report, accuracy_score

pitches = pd.read_csv('/TM24Szn(in).csv')
pitches.head()

print(pitches.iloc[:, 30:48])

x = pitches.iloc[:, 30:48].join(pitches.iloc[:, 7])
x = x.drop(['Tilt'], axis=1)
x.head()

xL = x[x['PitcherThrows'] == 'Left']
xR = x[x['PitcherThrows'] == 'Right']


xL = xL.drop(columns=['PitcherThrows'])
xR = xR.drop(columns=['PitcherThrows'])

print(xL.head)
print(xR.head)

y = pitches.iloc[:, 19].astype('category').cat.codes
y = pd.DataFrame({'target': y, 'PitcherThrows': pitches.iloc[:, 7]})


yL = y[y['PitcherThrows'] == 'Left']
yR = y[y['PitcherThrows'] == 'Right']


yL = yL.drop(columns=['PitcherThrows'])
yR = yR.drop(columns=['PitcherThrows'])
print(yL.head)
print(yR.head)

names = pitches.iloc[:, 19].astype('category')

# Get the codes from the categorical variable
codes = names.cat.codes

# Print the category mapping
category_mapping = {code: category for code, category in zip(range(len(names.cat.categories)), names.cat.categories)}
print(category_mapping)

from sklearn.model_selection import GridSearchCV


x_train_left, x_test_left, y_train_left, y_test_left = train_test_split(xL, yL, test_size=0.2, random_state=42)
x_train_right, x_test_right, y_train_right, y_test_right = train_test_split(xR, yR, test_size=0.2, random_state=42)

rf_left = RandomForestRegressor(random_state=42)
rf_right = RandomForestRegressor(random_state=42)

rf_param_grid = {
    'n_estimators': [100,300],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [None,10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

left_grid = GridSearchCV(estimator=rf_left, param_grid=rf_param_grid, cv=5, n_jobs=-1, verbose=2)
right_grid = GridSearchCV(estimator=rf_right, param_grid=rf_param_grid, cv=5, n_jobs=-1, verbose=2)

left_grid.fit(x_train_left, y_train_left.values.ravel())
right_grid.fit(x_train_right, y_train_right.values.ravel())

print("MSE for Left Data:")
print(mean_squared_error(y_test_left, left_grid.predict(x_test_left)))
print("MSE for Right Data:")
print(mean_squared_error(y_test_right, right_grid.predict(x_test_right)))
print("R2 Score for Left Data:")
print(r2_score(y_test_left, left_grid.predict(x_test_left)))
print("R2 Score for Right Data:")
print(r2_score(y_test_right, right_grid.predict(x_test_right)))

plt.scatter(y_test_left, left_grid.predict(x_test_left))
plt.xlabel('Left Pitch Actual Values')
plt.ylabel('Left Pitch Predicted Values')
plt.title('Actual vs. Predicted Values for Left Data')

plt.scatter(y_test_right, right_grid.predict(x_test_right))
plt.xlabel('Right Pitch Actual Values')
plt.ylabel('Right Pitch Predicted Values')
plt.title('Actual vs. Predicted Values for Right Data')

import pickle

with open('left_model.pkl', 'wb') as file:
    pickle.dump(left_grid, file)

with open('right_model.pkl', 'wb') as file:
    pickle.dump(right_grid, file)

files.download('left_model.pkl')
files.download('right_model.pkl')
#