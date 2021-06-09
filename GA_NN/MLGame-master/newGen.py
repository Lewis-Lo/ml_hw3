import pickle
from snake_v3 import Snake
import random
from genInfo import geninfo

def crossOver(s1, s2):
    child = Snake()
    index = random.random()

    for i in range(0, 24):
        for j in range(0, 16):
            child.L2_weight[i][j] = s1.L2_weight[i][j]
            child.L2_bias[i][j] = s1.L2_bias[i][j]
    for i in range(0, 16):
        for j in range(0, 3):
            child.L3_weight[i][j] = s1.L3_weight[i][j]
            child.L3_bias[i][j] = s1.L3_bias[i][j]

    if index < 0.25:
        split = random.randint(0, 24*16)
        for i in range(0, 24):
            for j in range(0, 16):
                if i*16 + j >= split:
                    child.L2_weight[i][j] = s2.L2_weight[i][j]

    elif index < 0.5:
        split = random.randint(0, 24*16)
        for i in range(0, 24):
            for j in range(0, 16):
                if i*16 + j >= split:
                    child.L2_bias[i][j] = s2.L2_bias[i][j]
    elif index < 0.75:
        split = random.randint(0, 16*3)
        for i in range(0, 16):
            for j in range(0, 3):
                if i*3 + j >= split:
                    child.L3_weight[i][j] = s2.L3_weight[i][j]
    else :
        split = random.randint(0, 16*3)
        for i in range(0, 16):
            for j in range(0, 3):
                if i*3 + j >= split:
                    child.L3_bias[i][j] = s2.L3_bias[i][j]

    return child

def newGen(snakes, genIndex):
    rk = []
    RK = []
    for i in range(0, 1000):
        count = 0
        for j in range(0, 3):
            if snakes[i].cc[j] <= 5 :
                count = count + 1
        if count == 0:
            snakes[i].fitness = snakes[i].fitness * 100
        elif count == 2:
            snakes[i].fitness = 0
    for i in range(0, 1000):
        if(snakes[i].score < 10) :
            snakes[i].fitness = (snakes[i].fitness ** 2) * pow(2,snakes[i].score)
        else :
            snakes[i].fitness = (snakes[i].fitness) * pow(2,10) * (snakes[i].score-9) * pow(2,snakes[i].score)
    
    gi = geninfo()
    gi.gen = (genIndex-1)
    for i in range(0, 1000):
        gi.score.append(snakes[i].score)
        gi.fitness.append(snakes[i].fitness)
    gi.dumpGeninfo()
    
    n = 0
    for j in range(0, 50):
        rk.append(0)
        for i in range(1, 1000-j-n):
            if snakes[i].fitness > snakes[rk[j]].fitness:
                rk[j] = i
        for k in range(0, len(RK)):
            if snakes[rk[j]].fitness == RK[k].fitness:
                snakes.remove(snakes[rk[j]])
                j = j - 1
                n = n + 1
                continue
        RK.append(snakes[rk[j]])
        snakes.remove(snakes[rk[j]])

    while len(RK) < 30:
        RK.append(Snake())

    newSnakes = []

    for i in range(0, 80):
        for j in range(0, 5):
            newSnakes.append(crossOver(RK[j], RK[j+1]))
    for i in range(0, 70):
        for j in range(6, 11):
            newSnakes.append(crossOver(RK[j], RK[j+1]))
    for i in range(0, 250):
        newSnakes.append(crossOver(RK[random.randint(0, 29)], RK[random.randint(0, 29)]))

        

    for i in range(0, 1000):
        if random.random() < 0.1:
            newSnakes[i].mutate()
        pickle.dump(newSnakes[i], open("Snake_g{}_{}_v3.pickle".format(genIndex, i+1), "wb"))





if __name__ == '__main__':
    s = []
    for i in range(0, 1000):
        s.append(Snake())
        s[i].fitness = i%100
    newGen(s, 2)