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

def newGen(RK1, RK2, RK3, RK4):
    snakeList = []
    rk1 = Snake()
    rk2 = Snake()
    rk3 = Snake()
    rk4 = Snake()

    for i in range(0, 16):
        for j in range(0, 24):
            rk1.L2_weight[i][j] = RK1.L2_weight[i][j]
            rk1.L2_bias[i][j] = RK1.L2_bias[i][j]
            rk2.L2_weight[i][j] = RK2.L2_weight[i][j]
            rk2.L2_bias[i][j] = RK2.L2_bias[i][j]
            rk3.L2_weight[i][j] = RK3.L2_weight[i][j]
            rk3.L2_bias[i][j] = RK3.L2_bias[i][j]
            rk4.L2_weight[i][j] = RK4.L2_weight[i][j]
            rk4.L2_bias[i][j] = RK4.L2_bias[i][j]
    for i in range(0, 16):
        for j in range(0, 16):
            rk1.L3_weight[i][j] = RK1.L3_weight[i][j]
            rk1.L3_bias[i][j] = RK1.L3_bias[i][j]
            rk2.L3_weight[i][j] = RK2.L3_weight[i][j]
            rk2.L3_bias[i][j] = RK2.L3_bias[i][j]
            rk3.L3_weight[i][j] = RK3.L3_weight[i][j]
            rk3.L3_bias[i][j] = RK3.L3_bias[i][j]
            rk4.L3_weight[i][j] = RK4.L3_weight[i][j]
            rk4.L3_bias[i][j] = RK4.L3_bias[i][j]
            
    for i in range(0, 4):
        for j in range(0, 16):
            rk1.L4_weight[i][j] = RK1.L4_weight[i][j]
            rk1.L4_bias[i][j] = RK1.L4_bias[i][j]
            rk2.L4_weight[i][j] = RK2.L4_weight[i][j]
            rk2.L4_bias[i][j] = RK2.L4_bias[i][j]
            rk3.L4_weight[i][j] = RK3.L4_weight[i][j]
            rk3.L4_bias[i][j] = RK3.L4_bias[i][j]
            rk4.L4_weight[i][j] = RK4.L4_weight[i][j]
            rk4.L4_bias[i][j] = RK4.L4_bias[i][j]
    
    for i in range(0, 5):
        snakeList.append(rk1)
        snakeList.append(rk2)
        snakeList.append(rk3)
        snakeList.append(rk4)
    for i in range(0, 30):
        off1, off2 = crossover(rk1, rk2)
        snakeList.append(off1)
        snakeList.append(off2)
    for i in range(0, 25):
        off1, off2 = crossover(rk1, rk3)
        snakeList.append(off1)
        snakeList.append(off2)
    for i in range(0, 20):
        off1, off2 = crossover(rk1, rk4)
        snakeList.append(off1)
        snakeList.append(off2)
    for i in range(0, 15):
        off1, off2 = crossover(rk2, rk3)
        snakeList.append(off1)
        snakeList.append(off2)
    for i in range(0, 200):
        snakeList[i].remake()
        if random.random() < 0.1:
            snakeList[i].mutate()

    return snakeList