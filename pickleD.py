from sklearn import svm
from sklearn import datasets
import pickle

clf = svm.SVC()
print("executing pickleD.py")
X, y = datasets.load_iris(return_X_y=True)
print("executing pickleD.py")
clf.fit(X, y)
print("executing pickleD.py")

file = open('model', 'wb')
pickle.dump(clf, file)
file.close()