import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = np.array(pickle.load(open("log_1.pickle", "rb")))
for i in range(2, 2):
    temp = np.array(pickle.load(open("log_{}.pickle".format(i), "rb")))
    data = np.vstack([data, temp])

for i in range(0, np.shape(data)[0]):
    data[i][0] = int(data[i][0])
    data[i][1] = int(data[i][1]) / 300
    data[i][2] = int(data[i][2]) / 300
    data[i][3] = int(data[i][3]) / 300
    data[i][4] = int(data[i][4]) / 300
    if data[i][5] == "UP":
        data[i][5] = 0
    elif data[i][5] == "DOWN":
        data[i][5] = 1
    elif data[i][5] == "LEFT":
        data[i][5] = 2
    elif data[i][5] == "RIGHT":
        data[i][5] = 3
    if data[i][6] == "UP":
        data[i][6] = 0
    elif data[i][6] == "DOWN":
        data[i][6] = 1
    elif data[i][6] == "LEFT":
        data[i][6] = 2
    elif data[i][6] == "RIGHT":
        data[i][6] = 3  

for i in range(1, np.shape(data)[0]):
    data[i][5] = data[i-1][5]
data = data[1:]

x = np.zeros((np.shape(data)[0], np.shape(data)[1] - 2))
y = np.zeros(np.shape(data)[0])
for i in range(0, np.shape(data)[0]):
    for j in range(0, 5):
        x[i][j] = data[i][j+1]
    y[i] = data[i][6]

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.33, random_state=42)

dtc = DecisionTreeClassifier()
dtc.fit(xTrain, yTrain)
print(dtc.score(xTest, yTest))

# pickle.dump(clf, open("mlp.pickle", "wb"))