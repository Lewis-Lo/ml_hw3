import pickle 
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

data = pickle.load(open("log_1.pickle", "rb"))
dataX = np.zeros((30000, 5))
dataY = np.zeros((30000, 1))

for i in range(0, 30000):
    cmd = 0
    if data[i][1] == "abUP":
        cmd = 0
    elif data[i][1] == "abDOWN":
        cmd = 1
    elif data[i][1] == "abLEFT":
        cmd = 2
    elif data[i][1] == "abRIGHT":
        cmd = 3
    temp = np.append(data[i][0], cmd)
    for j in range(0, 5):
        dataX[i][j] = temp[j]
    if data[i][2] == "UP":
        dataY[i] = 0
    elif data[i][2] == "DOWN":
        dataY[i] = 1
    elif data[i][2] == "LEFT":
        dataY[i] = 2
    elif data[i][2] == "RIGHT":
        dataY[i] = 3
    elif data[i][2] == "NONE":
        dataY[i] = 4
dataY = np.reshape(dataY, (30000))

xtrain = np.zeros((21000, 5))
ytrain = np.zeros((21000, 1))
xtest = np.zeros((9000, 5))
ytest = np.zeros((9000, 1))
for i in range(0, 30000):
    for j in range(0, 5):
        if i < 21000:
            xtrain[i][j] = dataX[i][j]
        else :
            xtest[i-21000][j] = dataX[i][j]
    if i < 21000:
        ytrain[i] = dataY[i]
    else :
        ytest[i-21000] = dataY[i]

dtc = DecisionTreeClassifier()
dtc.fit(xtrain, ytrain)
count = [0, 0, 0, 0, 0]
for i in range(0, len(xtest)):
    x = np.reshape(xtest[i], (1, 5))
    k = int(dtc.predict(x))
    count[k] = count[k] + 1
print(count)
pickle.dump(dtc, open("model.pickle", "wb"))

tx = [30, 1, 6, 25, 3]
tx = np.reshape(tx, (1, 5))
print(dtc.predict(tx))