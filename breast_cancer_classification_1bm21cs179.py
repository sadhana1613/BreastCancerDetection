# -*- coding: utf-8 -*-
"""Breast Cancer classification_1BM21CS179.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tr1DLBcSLfdGCeBW94Kjitm0A5k2okwp

Importing dependencies
"""

import numpy as np
import pandas as pd
import sklearn.datasets
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

"""Data collection and Processing"""

# loading data from sklearn
breast_cancer_dataset = sklearn.datasets.load_breast_cancer()

print(breast_cancer_dataset)

# loading the data to a data frame
data_frame=pd.DataFrame(breast_cancer_dataset.data, columns=breast_cancer_dataset.feature_names)

#print the first 5 rows of above data frame
data_frame.head()

#adding target column in the dataframe
data_frame['Diagnosis']=breast_cancer_dataset.target

# number of rows and columns in the dataset(gives a tuple)
data_frame.shape

# getting some information about the data
data_frame.info()

# checking for missing values
data_frame.isnull().sum()

# statistical measures about the data
data_frame.describe()

# checking the distribution of Target Varibale
data_frame['Diagnosis'].value_counts()

"""
*   1 represents Benign  (B in kaggle dataset)
*   0 represents Malignant  (M in kaggle dataset)

"""

data_frame.corr()

"""Thus, from the above correlation table, we see that mean radius, mean area, mean perimeter and mean concave points have a high correlation with malignant tumor."""

plt.figure(figsize=(20,20))
sns.heatmap(data_frame.corr(), annot=True)

cols = ['Diagnosis',
        'mean radius',
        'mean texture',
        'mean perimeter',
        'mean area',
        'mean smoothness',
        'mean compactness',
        'mean concavity',
        'mean concave points',
        'mean symmetry',
        'mean fractal dimension']

sns.pairplot(data=data_frame[cols], hue='Diagnosis', palette='rocket')

"""Almost perfect linear patterns between the radius, perimeter and area attributes are hinting at the presence of multicollinearity between these variables. Another set of variables that possibly imply multicollinearity are the concavity, concave_points and compactness.

Multicollinearity is a problem as it undermines the significance of independent variables and we fix it by removing the highly correlated predictors from the model by using methods that cut the number of predictors to a smaller set of uncorrelated components.
"""

# Generate and visualize the correlation matrix
corr = data_frame.corr().round(2)

# Mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set figure size
f, ax = plt.subplots(figsize=(20, 20))

# Define custom colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

plt.tight_layout()

"""We can verify the presence of multicollinearity between some of the variables. For instance, the radius_mean column has a correlation of 1 and 0.99 with perimeter_mean and area_mean columns, respectively. This is because the three columns essentially contain the same information, which is the physical size of the observation (the cell). Therefore we should only pick one of the three columns when we go into further analysis.

Another place where multicollinearity is apparent between the "mean" columns and the "worst" column. For instance, the radius_mean column has a correlation of 0.97 with the radius_worst column.

Also there is multicollinearity between the attributes compactness, concavity, and concave points.
"""

# first, drop all "worst" columns
cols = ['worst radius',
        'worst texture',
        'worst perimeter',
        'worst area',
        'worst smoothness',
        'worst compactness',
        'worst concavity',
        'worst concave points',
        'worst symmetry',
        'worst fractal dimension']
data_frame = data_frame.drop(cols, axis=1)

# then, drop all columns related to the "perimeter" and "area" attributes
cols = ['mean perimeter',
        'perimeter error',
        'mean area',
        'area error']
data_frame = data_frame.drop(cols, axis=1)

# lastly, drop all columns related to the "concavity" and "concave points" attributes
cols = ['mean concavity',
        'concavity error',
        'mean concave points',
        'concave points error']
data_frame = data_frame.drop(cols, axis=1)

# verify remaining columns
data_frame.columns

# Draw the heatmap again, with the new correlation matrix
corr = data_frame.corr().round(2)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

f, ax = plt.subplots(figsize=(20, 20))
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
plt.tight_layout()

"""Separating the features(x) and target(y)"""

X = data_frame.drop(columns='Diagnosis', axis=1)
Y = data_frame['Diagnosis']

print(X)

print(Y)

"""Splitting data into 'Training data' and 'Testing data'"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=5)

print(X.shape, X_train.shape, X_test.shape)

"""Feature Scaling"""

from sklearn.preprocessing import StandardScaler
ss=StandardScaler()

X_train=ss.fit_transform(X_train)
X_test=ss.fit_transform(X_test)

"""Model Training

Logistic Regression
"""

model = LogisticRegression()

# training the Logistic Regression model using Training data

model.fit(X_train, Y_train)

"""Model Evaluation

Accuracy score
"""

# accuracy on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

print('Accuracy on training data = ', training_data_accuracy)

# accuracy on test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print('Accuracy on test data = ', test_data_accuracy)

#confusion matrix
from sklearn.metrics import confusion_matrix

cm=confusion_matrix(Y_test,X_test_prediction)
sns.heatmap(cm/np.sum(cm), annot=True,
            fmt='.2%', cmap='Blues')

"""Building a Predictive System"""

input_data = (19.81,22.15,130,1260,0.09831,0.1027,0.1479,0.09498,0.1582,0.05395,0.7582,1.017,5.865,112.4,0.006494,0.01893,0.03391,0.01521,0.01356,0.001997,27.32,30.88,186.8,2398,0.1512,0.315,0.5372,0.2388,0.2768,0.07615)
# above input data is taken from csv file excluding id and label/diagnosis

# change the input data to a numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the numpy array as we are predicting for one datapoint
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = model.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('Malignant case')

else:
  print('Benign case')

"""KNN Classifier Model

Model Training
"""

knn=KNeighborsClassifier()

knn.fit(X_train,Y_train)

# accuracy on training data
X_train_prediction = knn.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

print('Accuracy on training data = ', training_data_accuracy)

# accuracy on test data
X_test_prediction = knn.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print('Accuracy on test data = ', test_data_accuracy)

#confusion matrix
from sklearn.metrics import confusion_matrix

cm=confusion_matrix(Y_test,X_test_prediction)
sns.heatmap(cm/np.sum(cm), annot=True,
            fmt='.2%', cmap='Blues')

"""Model Evaluation by accuracy score"""

#for different values of k-
no_neighbors = range(1,16)
training_accuracy=[]
test_accuracy=[]

for n in no_neighbors:
  knn=KNeighborsClassifier(n)
  knn.fit(X_train,Y_train)
  training_accuracy.append(accuracy_score(Y_train,knn.predict(X_train)))
  test_accuracy.append(accuracy_score(Y_test,knn.predict(X_test)))

kdata = {'k-value':no_neighbors, 'Training data accuracy': training_accuracy, 'Testing data accuracy': test_accuracy}
kdf = pd.DataFrame(data=kdata)
kdf

"""Effect of k-values to accuracy score"""

plt.plot(no_neighbors,training_accuracy,label="Training Data Accuracy")
plt.plot(no_neighbors,test_accuracy,label="Testing Data Accuracy")
plt.legend()
plt.plot()

training_accuracy[3]

test_accuracy[3]

"""Support Vector Machine"""

svm=SVC()

svm.fit(X_train,Y_train)
# accuracy on training data
X_train_prediction = svm.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)
# accuracy on test data
X_test_prediction = svm.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print('Accuracy on training data = ', training_data_accuracy)

print('Accuracy on test data = ', test_data_accuracy)

#confusion matrix
from sklearn.metrics import confusion_matrix

cm=confusion_matrix(Y_test,X_test_prediction)
sns.heatmap(cm/np.sum(cm), annot=True,
            fmt='.2%', cmap='Blues')

"""Conclusion: We are getting the best accuracy on our test data with Logistic Regression Model which is 96.5% ."""