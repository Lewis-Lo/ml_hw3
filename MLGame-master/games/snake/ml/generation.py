from snake import Snake
import random
import numpy as np

def crossover(mom, dad):
    offspringM = Snake()
    offspringM.copySnake(mom)
    offspringD = Snake()
    offspringD.copySnake(mom)

    for i in range(0, 16):
        for j in range(0, 24):
            if(random.random() < 0.1):
                temp = offspringM.L2_weight[i][j]
                offspringM.L2_weight[i][j] = offspringD.L2_weight[i][j]
                offspringD.L2_weight[i][j] = temp
            if(random.random() < 0.1):
                temp = offspringM.L2_bias[i][j]
                offspringM.L2_bias[i][j] = offspringD.L2_bias[i][j]
                offspringD.L2_bias[i][j] = temp
    for i in range(0, 16):
        for j in range(0, 16):
            if(random.random() < 0.1):
                temp = offspringM.L3_weight[i][j]
                offspringM.L3_weight[i][j] = offspringD.L3_weight[i][j]
                offspringD.L3_weight[i][j] = temp
            if(random.random() < 0.1):
                temp = offspringM.L3_bias[i][j]
                offspringM.L3_bias[i][j] = offspringD.L3_bias[i][j]
                offspringD.L3_bias[i][j] = temp
    for i in range(0, 4):
        for j in range(0, 16):
            if(random.random() < 0.1):
                temp = offspringM.L4_weight[i][j]
                offspringM.L4_weight[i][j] = offspringD.L4_weight[i][j]
                offspringD.L4_weight[i][j] = temp
            if(random.random() < 0.1):
                temp = offspringM.L4_bias[i][j]
                offspringM.L4_bias[i][j] = offspringD.L4_bias[i][j]
                offspringD.L4_bias[i][j] = temp

    return offspringM, offspringD