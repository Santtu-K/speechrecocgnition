#Importing libraries used in this project
import python_speech_features #NOTE delete later
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

#Read the training and validation data
data = pd.read_csv('all.csv')
#data.drop(range(450,4950), inplace=True)
#data.reset_index(drop=True)
#print(np.shape(data)) #NOTE Debug print

#Read the labels
labels = pd.read_csv('allLabels.csv')
true_numbers = labels.iloc[:4950].to_numpy()
true_numbers = np.nan_to_num(true_numbers)

#Define constant for creating a matrix
mfcc_vec_len = 2028 #NOTE This has to be the same length as "mfccdata" after flatten

#Initializing a matrix for data after mfcc process
data_matrix = np.zeros([np.shape(data)[0],mfcc_vec_len])
#print(np.shape(data_matrix)) #NOTE Debug print

#Loop through all datapoints
for n in range(np.shape(data)[0]):
    #Take in one datapoint
    mfccdata = data.iloc[[n]].to_numpy()
    #Implement MFCC
    mfccdata = python_speech_features.mfcc(mfccdata, 6000)
    #Flattening the matrix from mfcc function into a vector
    mfccdata = mfccdata.flatten()
    #print(np.shape(mfccdata)) #NOTE debug print

    #Append the matrix with all modified data
    data_matrix[n,:] = mfccdata

#Preprocess data for machine learning
#data_matrix_final = data_matrix[:,0:168] #NOTE used for taking out data if needed
data_matrix_final = np.nan_to_num(data_matrix)

#Defining features and the label
X = data_matrix_final
y = true_numbers

#print(np.shape(X)) #NOTE debug print

#Calculating the optimal split for test and validation sets
split_ratio = 1/np.sqrt(np.shape(data_matrix)[1])
#print(split_ratio) #NOTE Debug print


#Splittin the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split_ratio, random_state=42)

#X_val = X[:449]
#X_train = X[450:]
#y_val = y[:449]
#y_train = y[450:]
#print(np.shape(X_train)) #NOTE Debug print
#print(np.shape(y_train)) #NOTE Debug print

#Fitting a logistic regression model
lrmodel = LogisticRegression()
lrmodel.fit(X_train, y_train)

#Fitting an MLP classifier model NOTE this was worse than logistic regression
#num_neurons = 20
#num = 20
#layer_size = tuple([num_neurons]*num)
#lrmodel = MLPClassifier(hidden_layer_sizes=layer_size,random_state=42, max_iter=1000).fit(X_train,y_train)

#Checking the accuracy
y_train_pred = lrmodel.predict(X_train)
y_train_accuracy = accuracy_score(y_train, y_train_pred)
print("Training accuracy:", y_train_accuracy)

#Checking the validation accuracy
y_val_pred = lrmodel.predict(X_val)
y_val_accuracy = accuracy_score(y_val, y_val_pred)
print("Validation accuracy:", y_val_accuracy)

#Showing a confusion matrix
ax = plt.subplot()
c_mat = confusion_matrix(y_val, y_val_pred)
sns.heatmap(c_mat, annot=True, fmt='g', ax=ax)

#Save the trained machine learning model in a file
file = open('mlmodel', 'wb')
pickle.dump(lrmodel, file)
file.close()