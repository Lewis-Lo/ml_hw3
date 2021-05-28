import numpy as np
import random

class Snake:
    def __init__(self):
        score = 0
        L2_weight = np.zeros((16, 24))
        L2_bias = np.zeros((16, 24))
        L3_weight = np.zeros((16, 16))
        L3_bias = np.zeros((16, 16))
        L4_weight = np.zeros((4, 16))
        L4_bias = np.zeros((4, 16))
    
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

    def sigmoid(self, x):
        return 1/(np.exp(-1*x) + 1)

    def move(self, input):
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
            output = output + self.sigmoid(input[i] * self.L2_weight[index][i] + self.L2_bias[index][i])
        return output

    def layer_2(self, input):
        output = np.zeros(16)
        for i in range(0, 16):
            output[i] = self.neuron_2(input, i)
        return output

    def neuron_3(self, input, index):
        output = 0
        for i in range(0, 16):
            output = output + self.sigmoid(input[i] * self.L3_weight[index][i] + self.L3_bias[index][i])
        return output

    def layer_3(self, input):
        output = np.zeros(16)
        for i in range(0, 16):
            output[i] = self.neuron_3(input, i)
        return output
        
    def neuron_4(self, input, index):
        output = 0
        for i in range(0, 16):
            output = output + self.sigmoid(input[i] * self.L4_weight[index][i] + self.L4_bias[index][i])
        return output

    def layer_4(self, input):
        output = np.zeros(4)
        for i in range(0, 4):
            output[i] = self.neuron_3(input, i)
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

        output[4] = min(snakeHead[0], 30 - snakeHead[1])
        output[5] = output[6] = 0
        for i in range(1, int(output[4])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] + i == food[1])):
                output[5] = i
                break
        for i in range(1, int(output[4])):
            if(grid[snakeHead[0] - i][snakeHead[1] + i] == 2):
                output[6] = i
                break

        output[7] = 30 - snakeHead[1]
        output[8] = output[9] = 0
        for i in range(1, int(output[7])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] + i == food[1])):
                output[8] = i
                break
        for i in range(1, int(output[7])):
            if(grid[snakeHead[0]][snakeHead[1] + i] == 2):
                output[9] = i
                break

        output[10] = min(30 - snakeHead[0], 30 - snakeHead[1])
        output[11] = output[12] = 0
        for i in range(1, int(output[10])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] + i == food[1])):
                output[11] = i
                break
        for i in range(1, int(output[10])):
            if(grid[snakeHead[0] + i][snakeHead[1] + i] == 2):
                output[12] = i
                break

        output[13] = 30 - snakeHead[0]
        output[14] = output[15] = 0
        for i in range(1, int(output[13])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1]== food[1])):
                output[14] = i
                break
        for i in range(1, int(output[13])):
            if(grid[snakeHead[0] + i][snakeHead[1]] == 2):
                output[15] = i
                break

        output[16] = min(30 - snakeHead[0], snakeHead[1])
        output[17] = output[18] = 0
        for i in range(1, int(output[16])):
            if((snakeHead[0] + i == food[0]) and (snakeHead[1] - i == food[1])):
                output[17] = i
                break
        for i in range(1, int(output[16])):
            if(grid[snakeHead[0] + i][snakeHead[1] - i] == 2):
                output[18] = i
                break

        output[19] = snakeHead[1]
        output[20] = output[21] = 0
        for i in range(1, int(output[19])):
            if((snakeHead[0] == food[0]) and (snakeHead[1] - i == food[1])):
                output[20] = i
                break
        for i in range(1, int(output[19])):
            if(grid[snakeHead[0]][snakeHead[1] - i] == 2):
                output[21] = i
                break

        output[22] = min(snakeHead[0], snakeHead[1])
        output[23] = output[24] = 0
        for i in range(1, int(output[22])):
            if((snakeHead[0] - i == food[0]) and (snakeHead[1] - i == food[1])):
                output[23] = i
                break
        for i in range(1, int(output[22])):
            if(grid[snakeHead[0] - i][snakeHead[1] - i] == 2):
                output[24] = i
                break

        return output