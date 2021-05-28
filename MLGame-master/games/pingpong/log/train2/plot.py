import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

#load log資料夾中的一個pickle檔

with open("ml_HARD_100_2021-05-06_00-38-05.pickle", "rb") as file:
    log = pickle.load(file)

length = len(log['ml_1P']['command'])

Frames = np.zeros([length])
BallX = np.zeros([length])
BallY = np.zeros([length])
BallSpeedX = np.zeros([length])
BallSpeedY = np.zeros([length])
P1X = np.zeros([length])
P2X = np.zeros([length])
blockerX = np.zeros([length])
blockerY = np.zeros([length])
command1P = np.zeros([length])
command2P = np.zeros([length])
ballDir = np.zeros([length])
blockerDir = np.zeros([length])

for i in range(0, length-1):
        Frames[i] = log['ml_1P']['scene_info'][i]['frame']
        BallX[i] = log['ml_1P']['scene_info'][i]['ball'][0]
        BallY[i] = log['ml_1P']['scene_info'][i]['ball'][1]
        BallSpeedX[i] = log['ml_1P']['scene_info'][i]['ball_speed'][0]
        BallSpeedY[i] = log['ml_1P']['scene_info'][i]['ball_speed'][1]
        P1X[i] = log['ml_1P']['scene_info'][i]['platform_1P'][0]
        P2X[i] = log['ml_1P']['scene_info'][i]['platform_2P'][0]
        blockerX[i] = log['ml_1P']['scene_info'][i]['blocker'][0]
        blockerY[i] = log['ml_1P']['scene_info'][i]['blocker'][1]
        temp = log['ml_1P']['command'][i]
        if(temp == 'SERVE_TO_LEFT'):
            command1P[i] = 0
        elif(temp == 'SERVE_TO_RIGHT'):
            command1P[i] = 1
        elif(temp == 'MOVE_LEFT'):
            command1P[i] = 2
        elif(temp == 'MOVE_RIGHT'):
            command1P[i] = 3
        else:
            command1P[i] = 4
        temp = log['ml_2P']['command'][i]
        if(temp == 'SERVE_TO_LEFT'):
            command2P[i] = 0
        elif(temp == 'SERVE_TO_RIGHT'):
            command2P[i] = 1
        elif(temp == 'MOVE_LEFT'):
            command2P[i] = 2
        elif(temp == 'MOVE_RIGHT'):
            command2P[i] = 3
        else:
            command2P[i] = 4
        if(i != 0):
            if(blockerX[i] - blockerX[i-1] > 0):
                blockerDir[i] = 1   # right
            else:
                blockerDir[i] = -1  #left

            # dir : 0:右上, 1:右下, 2:左上, 3:左下
            deltaBall = [0, 0]
            deltaBall[0] = BallX[i] - BallX[i-1]
            deltaBall[1] = BallY[i] - BallY[i-1]
            if(deltaBall[0] > 0 and deltaBall[1] < 0):
                ballDir[i] = 0
            elif(deltaBall[0] > 0 and deltaBall[1] > 0):
                ballDir[i] = 1
            elif(deltaBall[0] < 0 and deltaBall[1] < 0):
                ballDir[i] = 2
            elif(deltaBall[0] < 0 and deltaBall[1] > 0):
                ballDir[i] = 3
        
BallX = BallX[1:]    
BallY = BallY[1:]
BallSpeedX = BallSpeedX[1:]    
BallSpeedY = BallSpeedY[1:]
P1X = P1X[1:]    
P2X = P2X[1:]    
blockerX = blockerX[1:]
blockerDir = blockerDir[1:]
ballDir = ballDir[1:]
command1P = command1P[1:]
command2P = command2P[1:]

with open("dtcP1.pickle", "rb") as file:
    model = pickle.load(file)
features = np.array([BallX, BallY, BallSpeedX, BallSpeedY, P1X, P2X, blockerX, blockerDir, ballDir, command1P, command2P])
predict = np.zeros([length - 1])
for i in range(0, length-1):
    test = np.zeros((1, 9))
    test[0, 0] = BallX[i]
    test[0, 1] = BallY[i]
    test[0, 2] = BallSpeedX[i]
    test[0, 3] = BallSpeedY[i]
    test[0, 4] = P1X[i]
    test[0, 5] = P2X[i]
    test[0, 6] = blockerX[i]
    test[0, 7] = blockerDir[i]
    test[0, 8] = ballDir[i]
    d = test[0, [0, 1, 2, 3, 4, 5, 6, 7, 8]].reshape(1, -1)
    predict[i] = model.predict(d)


for i in range(0, length-1):
    if(command1P[i] == 2):
        c1 = plt.scatter(BallX[i], BallY[i], c='r', marker='+')
    if(command1P[i] == 3):
        c2 = plt.scatter(BallX[i], BallY[i], c='b', marker='*')
    if(command1P[i] == 4):
        c3 = plt.scatter(BallX[i], BallY[i], c='g', marker='o')
plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballX')
plt.ylabel('ballY')
plt.title('rule')
plt.show()

for i in range(0, length-1):
    if(predict[i] == 2):
        c1 = plt.scatter(BallX[i], BallY[i], c='r', marker='+')
    if(predict[i] == 3):
        c2 = plt.scatter(BallX[i], BallY[i], c='b', marker='*')
    if(predict[i] == 4):
        c3 = plt.scatter(BallX[i], BallY[i], c='g', marker='o')
        plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballX')
plt.ylabel('ballY')
plt.title('model')
plt.show()

for i in range(0, length-1):
    if(command1P[i] == 2):
        c1 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='r', marker='+')
    if(command1P[i] == 3):
        c2 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='b', marker='*')
    if(command1P[i] == 4):
        c3 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='g', marker='o')
plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballSpeedX')
plt.ylabel('ballSpeedY')
plt.title('rule')
plt.show()

for i in range(0, length-1):
    if(predict[i] == 2):
        c1 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='r', marker='+')
    if(predict[i] == 3):
        c2 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='b', marker='*')
    if(predict[i] == 4):
        c3 = plt.scatter(BallSpeedX[i], BallSpeedY[i], c='g', marker='o')
        plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballSpeedX')
plt.ylabel('ballSpeedY')
plt.title('model')
plt.show()

for i in range(0, length-1):
    if(command1P[i] == 2):
        c1 = plt.scatter(P1X[i], P2X[i], c='r', marker='+')
    if(command1P[i] == 3):
        c2 = plt.scatter(P1X[i], P2X[i], c='b', marker='*')
    if(command1P[i] == 4):
        c3 = plt.scatter(P1X[i], P2X[i], c='g', marker='o')
plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('P1X')
plt.ylabel('P1Y')
plt.title('rule')
plt.show()

for i in range(0, length-1):
    if(predict[i] == 2):
        c1 = plt.scatter(P1X[i], P2X[i], c='r', marker='+')
    if(predict[i] == 3):
        c2 = plt.scatter(P1X[i], P2X[i], c='b', marker='*')
    if(predict[i] == 4):
        c3 = plt.scatter(P1X[i], P2X[i], c='g', marker='o')
        plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('P1X')
plt.ylabel('P2Y')
plt.title('model')
plt.show()

for i in range(0, length-1):
    if(command1P[i] == 2):
        c1 = plt.scatter(blockerX[i], blockerDir[i], c='r', marker='+')
    if(command1P[i] == 3):
        c2 = plt.scatter(blockerX[i], blockerDir[i], c='b', marker='*')
    if(command1P[i] == 4):
        c3 = plt.scatter(blockerX[i], blockerDir[i], c='g', marker='o')
plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('blockerX')
plt.ylabel('blockerDir')
plt.title('rule')
plt.show()

for i in range(0, length-1):
    if(predict[i] == 2):
        c1 = plt.scatter(blockerX[i], blockerDir[i], c='r', marker='+')
    if(predict[i] == 3):
        c2 = plt.scatter(blockerX[i], blockerDir[i], c='b', marker='*')
    if(predict[i] == 4):
        c3 = plt.scatter(blockerX[i], blockerDir[i], c='g', marker='o')
        plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('blockerX')
plt.ylabel('blockerDir')
plt.title('model')
plt.show()

for i in range(0, length-1):
    if(command1P[i] == 2):
        c1 = plt.scatter(ballDir[i], blockerDir[i], c='r', marker='+')
    if(command1P[i] == 3):
        c2 = plt.scatter(ballDir[i], blockerDir[i], c='b', marker='*')
    if(command1P[i] == 4):
        c3 = plt.scatter(ballDir[i], blockerDir[i], c='g', marker='o')
plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballDir')
plt.ylabel('blockerDir')
plt.title('rule')
plt.show()

for i in range(0, length-1):
    if(predict[i] == 2):
        c1 = plt.scatter(ballDir[i], blockerDir[i], c='r', marker='+')
    if(predict[i] == 3):
        c2 = plt.scatter(ballDir[i], blockerDir[i], c='b', marker='*')
    if(predict[i] == 4):
        c3 = plt.scatter(ballDir[i], blockerDir[i], c='g', marker='o')
        plt.legend([c1, c2, c3], ['LEFT', 'RIGHT', 'NONE'])
plt.xlabel('ballDir')
plt.ylabel('blockerDir')
plt.title('model')
plt.show()