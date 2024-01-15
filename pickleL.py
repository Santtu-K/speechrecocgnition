import pickle
from sklearn import datasets

X, y = datasets.load_iris(return_X_y=True)

file = open('model', 'rb')
clf2 = pickle.load(file)
file.close()
print(f'predicted: {clf2.predict(X[0:1])}')
print(f'actual: {y[0]}')