import pickle 
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
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


ks = [1, 3, 5, 7, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
scores = []
for i in range(0, len(ks)):
    knn = KNeighborsClassifier(n_neighbors=ks[i])
    knn.fit(xtrain, ytrain)

    scores.append(knn.score(xtest, ytest))

plt.plot(ks, scores)
plt.xlabel("n_neighbors")
plt.ylabel("model score")
plt.show()





















dataX = np.zeros((100000, 5))
dataY = np.zeros((100000, 1))

for i in range(0, 100000):
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
dataY = np.reshape(dataY, (100000))

xtrain, xtest, ytrain, ytest = train_test_split(dataX, dataY, test_size=0.3)

ks = [3, 5, 10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
scores = []
for i in range(0, len(ks)):
    print(ks[i])
    knn = KNeighborsClassifier(n_neighbors=ks[i])
    knn.fit(xtrain, ytrain)

    scores.append(knn.score(xtest, ytest))

plt.plot(ks, scores)
plt.xlabel("n_neighbors")
plt.ylabel("model score")
plt.show()