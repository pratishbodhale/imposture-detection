# Imposture Detection

Authenticate the user by training and testing one class SVM classifier by the data acquired with neutral mood.

mood_data_extractor.py : Extract useful features from mood files and generate .txt files similiar to continuos data collection 'preproc_data' folder  

featurematrix.py : Returns a data frame of (hold time, latencies) for all the characters text files in mood data. 

One_Class_SVM.py : Get the data in the format of dataframe and train the model using full neutral data. Further calculated test accuracy for three different data sets (Continuos, Happy, Sad)

Cross_Vaidation.py: Split the neutral data in 5 parts and perform the 5 fold cross validation to obtain the model accuracy.
