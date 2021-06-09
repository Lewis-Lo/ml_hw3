import numpy as np
import random
import math

class Snake:
    def __init__(self):
        self.historyScore = []
        self.fitness = 0
        self.score = 0
        self.L2_weight = np.zeros((24, 16))
        self.L2_bias = np.zeros((24, 16))
        self.L3_weight = np.zeros((16, 3))
        self.L3_bias = np.zeros((16, 3))
        self.cc = [0, 0, 0]
        self.loop = 0
 
        self.leftStep = 150
        for i in range(0, 24):
            for j in range(0, 16):
                self.L2_weight[i][j] = random.uniform(-1, 1)
                self.L2_bias[i][j] = random.uniform(-1, 1)
        for i in range(0, 16):
            for j in range(0, 3):
                self.L3_weight[i][j] = random.uniform(-1, 1)
                self.L3_bias[i][j] = random.uniform(-1, 1)

    def remake(self):
        self.historyScore.append(self.fitness)
        self.fitness = 0
        self.leftStep = 150

    def getAvgScore(self):
        return np.mean(self.historyScore)

    def mutate(self):
        index = random.random()
        s2 = Snake()

        if index < 0.25:
            split = random.randint(0, 24*16)
            for i in range(0, 24):
                for j in range(0, 16):
                    if i*16 + j >= split:
                        self.L2_weight[i][j] = s2.L2_weight[i][j]

        elif index < 0.5:
            split = random.randint(0, 24*16)
            for i in range(0, 24):
                for j in range(0, 16):
                    if i*16 + j >= split:
                        self.L2_bias[i][j] = s2.L2_bias[i][j]
        elif index < 0.75:
            split = random.randint(0, 16*3)
            for i in range(0, 16):
                for j in range(0, 3):
                    if i*3 + j >= split:
                        self.L3_weight[i][j] = s2.L3_weight[i][j]
        else :
            split = random.randint(0, 16*3)
            for i in range(0, 16):
                for j in range(0, 3):
                    if i*3 + j >= split:
                        self.L3_bias[i][j] = s2.L3_bias[i][j]

    def sigmoid(self, x):
        return 1/(np.exp(-1*x) + 1)

    def relu(self, x):
        return max(0, x)

    def getApple(self):
        self.leftStep = self.leftStep + 200
        self.score = self.score + 1
        self.loop = 0

    def move(self, input, hDir):
        self.leftStep = self.leftStep - 1
        self.loop = self.loop + 1
        if(self.leftStep <= 0):
            return "NONE"
        self.fitness = self.fitness + 0.5

        L2out = self.layer_2(input)
        L3out = self.layer_3(L2out)        

        if input[16] == 1 or input[19] == 1 or input[22] == 1:
            L3out[1] = L3out[1] + 5
        elif input[4] == 1 or input[7] == 1 or input[10] == 1:
            L3out[2] = L3out[2] + 5
        elif input[1] == 1:
            L3out[0] = L3out[0] + 5
            if input[0] <= 0.04:
                L3out[0] = L3out[0] - 5

        if self.loop >= 300:
            self.loop = 0
            ind = 0
            if(min(L3out) == L3out[0]):
                ind = 0
            if(min(L3out) == L3out[1]):
                ind = 1
            if(min(L3out) == L3out[2]): 
                ind = 2
            for i in range(0, 3):
                L3out[i] = 0
            L3out[ind] = 1

        if(max(L3out) == L3out[0]):
            self.cc[0] = self.cc[0] + 1
            return "NONE"
        if(max(L3out) == L3out[1]):
            self.cc[1] = self.cc[1] + 1
            if hDir == "abUP":
                return "LEFT"
            elif hDir == "abRIGHT":
                return "UP"
            elif hDir == "abDOWN":
                return "RIGHT"
            elif hDir == "abLEFT":
                return "DOWN"
        if(max(L3out) == L3out[2]):
            self.cc[2] = self.cc[2] + 1
            if hDir == "abUP":
                return "RIGHT"
            elif hDir == "abRIGHT":
                return "DOWN"
            elif hDir == "abDOWN":
                return "LEFT"
            elif hDir == "abLEFT":
                return "UP"

    def out_ori(self, input, hDir):
        self.leftStep = self.leftStep - 1
        if(self.leftStep <= 0):
            return "NONE"
        self.fitness = self.fitness + 0.1

        L2out = self.layer_2(input)
        L3out = self.layer_3(L2out)  
        if(max(L3out) == L3out[0]):
            return "NONE"
        if(max(L3out) == L3out[1]):
            return "TURN_LEFT"
        if(max(L3out) == L3out[2]):
            return "TURN_RIGHT"

    def neuron_2(self, input, index):
        output = 0
        for i in range(0, 24):
            output = output + (input[i] * self.L2_weight[i][index] + self.L2_bias[i][index])
        return self.relu(output)

    def layer_2(self, input):
        output = np.zeros(16)
        for i in range(0, 16):
            output[i] = self.neuron_2(input, i)
        return output

    def neuron_3(self, input, index):
        output = 0
        for i in range(0, 16):
            output = output + input[i] * self.L3_weight[i][index] + self.L3_bias[i][index]
        return self.relu(output)

    def layer_3(self, input):
        output = np.zeros(3)
        for i in range(0, 3):
            output[i] = self.neuron_3(input, i)

        return output

    def sensor(self, grid, hDir):
        output = np.zeros(24)
        snakeHead = [0, 0]
        food = [0, 0]
        for i in range(0, 30):
            for j in range(0, 30):
                if grid[i][j] == 1:
                    snakeHead[0] = i
                    snakeHead[1] = j
                if grid[i][j] == 3:
                    food[0] = i
                    food[1] = j

        output[0] = snakeHead[0] + 1
        output[1] = 0
        output[2] = 30
        for i in range(1, int(output[0])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] == food[1])):
                output[1] = 1
                break
        for i in range(1, int(output[0])):
            if(grid[snakeHead[0] - i][snakeHead[1]] == 2):
                output[2] = i
                break

        output[3] = min(snakeHead[0] + 1, 30 - snakeHead[1])
        output[4] = 0
        output[5] = 30
        for i in range(1, int(output[3])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] + i == food[1])):
                output[4] = 1
                break
        for i in range(1, int(output[3])):
            if(grid[snakeHead[0] - i][snakeHead[1] + i] == 2):
                output[5] = i
                break

        output[6] = 30 - snakeHead[1]
        output[7] = 0
        output[8] = 30
        for i in range(1, int(output[6])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] + i == food[1])):
                output[7] = 1
                break
        for i in range(1, int(output[6])):
            if(grid[snakeHead[0]][snakeHead[1] + i] == 2):
                output[8] = i
                break

        output[9] = min(30 - snakeHead[0], 30 - snakeHead[1])
        output[10] = 0
        output[11] = 30
        for i in range(1, int(output[9])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] + i == food[1])):
                output[10] = 1
                break
        for i in range(1, int(output[9])):
            if(grid[snakeHead[0] + i][snakeHead[1] + i] == 2):
                output[11] = i
                break

        output[12] = 30 - snakeHead[0]
        output[13] = 0
        output[14] = 30
        for i in range(1, int(output[12])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1]== food[1])):
                output[13] = 1
                break
        for i in range(1, int(output[12])):
            if(grid[snakeHead[0] + i][snakeHead[1]] == 2):
                output[14] = i
                break

        output[15] = min(30 - snakeHead[0], snakeHead[1] + 1)
        output[16] = 0
        output[17] = 30
        for i in range(1, int(output[15])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] - i == food[1])):
                output[16] = 1
                break
        for i in range(1, int(output[15])):
            if(grid[snakeHead[0] + i][snakeHead[1] - i] == 2):
                output[17] = i
                break

        output[18] = snakeHead[1] + 1
        output[19] = 0
        output[20] = 30
        for i in range(1, int(output[18])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] - i == food[1])):
                output[19] = 1
                break
        for i in range(1, int(output[18])):
            if(grid[snakeHead[0]][snakeHead[1] - i] == 2):
                output[20] = i
                break

        output[21] = min(snakeHead[0] + 1, snakeHead[1] + 1)
        output[22] = 0
        output[23] = 30
        for i in range(1, int(output[21])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] - i == food[1])):
                output[22] = 1
                break
        for i in range(1, int(output[21])):
            if(grid[snakeHead[0] - i][snakeHead[1] - i] == 2):
                output[23] = i
                break

        temp = np.zeros(48)
        for i in range(0, 24):
            temp[i] = output[i]
            temp[24 + i] = output[i]

        if hDir == "abUP":
           pass  

        if hDir == "abDOWN":
            for i in range(0, 24):
                output[i] = temp[i+12]

        if hDir == "abLEFT":
            for i in range(0, 24):
                output[i] = temp[i+18]
        
        if hDir == "abRIGHT":
            for i in range(0, 24):
                output[i] = temp[i+6]         

        for i in range(0, 24):
            if i%3 != 1:
                output[i] = round(output[i]/30, 2)

        return output