import os
import pickle
import numpy as np

yourPath = './'
allFileList = os.listdir(yourPath)

dataNum = len(allFileList) - 1
index = 0
for i in range(1, dataNum + 1):
    index = index + 1
    log = pickle.load(open(allFileList[i], 'rb'))

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

    features = np.array([BallX, BallY, BallSpeedX, BallSpeedY, P1X, P2X, blockerX, blockerDir, ballDir, command1P, command2P])
    pickle.dump(features, open('features{}.pickle'.format(str(index)), 'wb'))
    


