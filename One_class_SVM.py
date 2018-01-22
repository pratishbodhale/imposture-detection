#import all required libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import accuracy_score     #to calculate accuracy of prediction
import string
import pandas as pd
from featurematrix import feature_matrix
alphabet= list(string.ascii_uppercase)
import os

#path to the directory which has Neutral Data(training data)
train_path = "C:/Users/Pankaj/Desktop/Mies term project/Continuous data collection of keyboard and mouse/preproc_data/patel_MoodData/MoodData/Neutral/"

#path to the directory which has continues/happy/Sad Data(test data)
# test_path = "C:/Users/Pankaj/Desktop/Mies term project/Continuous data collection of keyboard and mouse/preproc_data/patel_MoodData/MoodData/Emotional/Sad/"
test_path = "C:/Users/Pankaj/Desktop/Mies term project/Continuous data collection of keyboard and mouse/preproc_data/Train data/"

#called Feature matrix function to obtain the dataframes with required feature(Hold_time & Latencies)
X_train= feature_matrix(train_path)
X_test= feature_matrix(test_path)

#train one class SVM using train dataset and predict the class of test dataset
training_labels = np.ones([len(X_train), 1])
testing_labels = np.ones([len(X_test), 1])
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
clf.fit(X_train)

y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)

#Accuracy
Training_Accuracy = accuracy_score(training_labels, y_pred_train) * 100
Testing_Accuracy =  accuracy_score(testing_labels, y_pred_test) * 100

print("Training accu :",Training_Accuracy)
print("Testing accu  :", Testing_Accuracy)
print("\n")

#plotting
xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-1, 3, 50))
# plot the line, the points, and the nearest vectors to the plane
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("One_class_SVM")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 5), cmap=plt.cm.PuBu)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')
s = 20
b1 = plt.scatter(X_train.iloc[:, 0], X_train.iloc[:, 1], c='white', s=s, edgecolors='k')
b2 = plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c='violet', s=s,edgecolors='k')
plt.axis('tight')
plt.legend([a.collections[0], b1, b2],["Decision Boundary", "training observations","test observation"],loc="upper left")
plt.xlabel("Training_Accuracy: %d%% ; Testing_Accuracy: %d%% ; " %(Training_Accuracy, Testing_Accuracy))
plt.show()