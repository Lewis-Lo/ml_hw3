from snake import Snake
import numpy as np
import os
import pickle

def selectSnake(generation):
    yourPath = './'
    allFileList = os.listdir(yourPath)
    toS = []
    scores = []
    selected = []
    for i in range(0, len(allFileList)):
        if("Snake_g{}".format(generation) in allFileList[i]):
            toS.append(allFileList[i])
            scores.append(0)

    for i in range(0, len(toS)):
        s = pickle.load(open(toS), 'rb')
        scores[i] = s.getScore()

def crossOver(mom, dad):


def mutation(snake):