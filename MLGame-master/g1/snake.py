import numpy as np
import random

class Snake:
    def __init__(self):
        self.score = 0
        self.L2_weight = np.zeros((16, 24))
        self.L2_bias = np.zeros((16, 24))
        self.L3_weight = np.zeros((16, 16))
        self.L3_bias = np.zeros((16, 16))
        self.L4_weight = np.zeros((4, 16))
        self.L4_bias = np.zeros((4, 16))
        self.leftStep = 300
        for i in range(0, 16):
            for j in range(0, 24):
                self.L2_weight[i][j] = random.random()
                self.L2_bias[i][j] = random.random()
        for i in range(0, 16):
            for j in range(0, 16):
                self.L3_weight[i][j] = random.random()
                self.L3_bias[i][j] = random.random()
        for i in range(0, 4):
            for j in range(0, 16):
                self.L4_weight[i][j] = random.random()
                self.L4_bias[i][j] = random.random()


        
    
    def random_gen(self):
        for i in self.L2_weight:
            i = random.randrange(0, 1)/24
        for i in self.L2_bias:
            i = random.randrange(0, 1)/24
        for i in self.L3_weight:
            i = random.randrange(0, 1)/16
        for i in self.L3_bias:
            i = random.randrange(0, 1)/16
        for i in self.L4_weight:
            i = random.randrange(0, 1)/4
        for i in self.L4_bias:
            i = random.randrange(0, 1)/4

    def getScore(self):
        return self.score

    def sigmoid(self, x):
        return 1/(np.exp(-1*x) + 1)

    def getApple(self):
        self.score = self.score + 1
        self.leftStep = self.leftStep + 100

    def move(self, input):
        self.leftStep = self.leftStep - 1
        if(self.leftStep <= 0):
            return "NONE"
        self.score = self.score + 0.01

        L2out = self.layer_2(input)
        L3out = self.layer_3(L2out)
        L4out = self.layer_4(L3out)

        if(max(L4out) == L4out[0]):
            return "UP"
        if(max(L4out) == L4out[1]):
            return "DOWN"
        if(max(L4out) == L4out[2]):
            return "LEFT"
        if(max(L4out) == L4out[3]):
            return "RIGHT"

    def neuron_2(self, input, index):
        output = 0
        for i in range(0, 24):
            output = output + (self.sigmoid(input[i] * self.L2_weight[index][i] + self.L2_bias[index][i]))/24
        return self.sigmoid(output)

    def layer_2(self, input):
        output = np.zeros(16)
        for i in range(0, 16):
            output[i] = self.neuron_2(input, i)
        return output

    def neuron_3(self, input, index):
        output = 0
        for i in range(0, 16):
            output = output + self.sigmoid(input[i] * self.L3_weight[index][i] + self.L3_bias[index][i])/16
        return self.sigmoid(output)

    def layer_3(self, input):
        output = np.zeros(16)
        for i in range(0, 16):
            output[i] = self.neuron_3(input, i)
        return output
        
    def neuron_4(self, input, index):
        output = 0
        for i in range(0, 16):
            output = output + self.sigmoid(input[i] * self.L4_weight[index][i] + self.L4_bias[index][i])/16
        return self.sigmoid(output)

    def layer_4(self, input):
        output = np.zeros(4)
        for i in range(0, 4):
            output[i] = self.neuron_4(input, i)
        return output

    def sensor(self, grid):
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

        output[0] = snakeHead[0]
        output[1] = output[2] = 0
        for i in range(1, int(output[0])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] == food[1])):
                output[1] = i
                break
        for i in range(1, int(output[0])):
            if(grid[snakeHead[0] - i][snakeHead[1]] == 2):
                output[2] = i
                break

        output[3] = min(snakeHead[0], 30 - snakeHead[1])
        output[4] = output[5] = 0
        for i in range(1, int(output[3])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] + i == food[1])):
                output[4] = i
                break
        for i in range(1, int(output[3])):
            if(grid[snakeHead[0] - i][snakeHead[1] + i] == 2):
                output[5] = i
                break

        output[6] = 30 - snakeHead[1]
        output[7] = output[8] = 0
        for i in range(1, int(output[6])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] + i == food[1])):
                output[7] = i
                break
        for i in range(1, int(output[6])):
            if(grid[snakeHead[0]][snakeHead[1] + i] == 2):
                output[8] = i
                break

        output[9] = min(30 - snakeHead[0], 30 - snakeHead[1])
        output[10] = output[11] = 0
        for i in range(1, int(output[9])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] + i == food[1])):
                output[10] = i
                break
        for i in range(1, int(output[9])):
            if(grid[snakeHead[0] + i][snakeHead[1] + i] == 2):
                output[11] = i
                break

        output[12] = 30 - snakeHead[0]
        output[13] = output[14] = 0
        for i in range(1, int(output[12])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1]== food[1])):
                output[13] = i
                break
        for i in range(1, int(output[12])):
            if(grid[snakeHead[0] + i][snakeHead[1]] == 2):
                output[14] = i
                break

        output[15] = min(30 - snakeHead[0], snakeHead[1])
        output[16] = output[17] = 0
        for i in range(1, int(output[15])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] - i == food[1])):
                output[16] = i
                break
        for i in range(1, int(output[15])):
            if(grid[snakeHead[0] + i][snakeHead[1] - i] == 2):
                output[17] = i
                break

        output[18] = snakeHead[1]
        output[19] = output[20] = 0
        for i in range(1, int(output[18])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] - i == food[1])):
                output[19] = i
                break
        for i in range(1, int(output[18])):
            if(grid[snakeHead[0]][snakeHead[1] - i] == 2):
                output[20] = i
                break

        output[21] = min(snakeHead[0], snakeHead[1])
        output[22] = output[23] = 0
        for i in range(1, int(output[21])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] - i == food[1])):
                output[22] = i
                break
        for i in range(1, int(output[21])):
            if(grid[snakeHead[0] - i][snakeHead[1] - i] == 2):
                output[23] = i
                break

        return output