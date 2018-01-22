#import all required libraries
import numpy as np
import matplotlib.pyplot as plt
import string
import pandas as pd
from sklearn import svm
from sklearn.metrics import accuracy_score     #to calculate accuracy of prediction
alphabet= list(string.ascii_uppercase)
from featurematrix import feature_matrix
import os

#path to the directory which has Neutral Data
path = "C:/Users/Pankaj/Desktop/Mies term project/Continuous data collection of keyboard and mouse/preproc_data/patel_MoodData/MoodData/Neutral/"

#called Feature matrix function to obtain the dataframe with required feature(Hold_time & Latencies)
data= feature_matrix(path)


#divide data into five interval for 5 fold cross validation
size = data.shape[0]
interval = np.ones([6], dtype=int)
val = int(size/ 5)
j = 0
for i in range(0, size - 1, val):
    interval[j] = int(i)
    j = j + 1

interval[5] = (size - 1)

# evertime use 1 differnt interval for testing and remaining 4 for training
for i in range(5):
    ind1 = interval[i]
    ind2 = interval[i + 1]

    #divide data into train and test set
    X_train = data[0:ind1][:].append(data[(ind2 + 1):][:], ignore_index=True)
    X_test = data[ind1 + 1:ind2][:]

    training_labels = np.ones([len(X_train), 1])
    testing_labels = np.ones([len(X_test), 1])

    #train one class SVM using train dataset and predict the class of dataset
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    clf.fit(X_train)

    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)

    #Accuracy of prediction
    Training_Accuracy = accuracy_score(training_labels, y_pred_train) * 100
    Testing_Accuracy =  accuracy_score(testing_labels, y_pred_test) * 100
    print("For set {0}: ".format(i + 1))
    print("Training accu :",Training_Accuracy)
    print("Testing accu  :", Testing_Accuracy)
    print("\n")

    #plotting
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-1, 3, 50))
    # plot the line, the points, and the nearest vectors to the plane
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.title("One_class_SVM_Cross_validation")
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