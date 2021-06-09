"""
The template of the script for playing the game in the ml mode
"""

import pickle
from snake_v3 import Snake
import numpy as np
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.grid = np.zeros((30, 30))
        self.state = 1
        self.s = Snake()
        self.sList = []
        self.generation = 8
        self.Index = 17
        self.tgrid = np.zeros((30, 30)) 
        self.preFood = [0, 0]
        self.dir = "DOWN"
        self.preDir = "DOWN"
        self.features = []
        self.target = []
        self.model = pickle.load(open("mlp.pickle", "rb"))
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            if len(scene_info["snake_body"]) >= 40:
                pickle.dump(self.features, open("log_{}.pickle".format(self.Index), "wb"))
                self.Index = self.Index + 1
            self.features = []
            self.state = 1
            self.dir = "DOWN"
            self.preDir = "DOWN"
            return "RESET"

        snake_head = scene_info["snake_head"]
        snake_body = scene_info["snake_body"]
        food = scene_info["food"]

        self.grid = np.zeros((30, 30))
        self.grid[int(snake_head[0]/10)][int(snake_head[1]/10)] = 1
        for i in snake_body:
            self.grid[int(i[0]/10)][int(i[1]/10)] = 2
        self.grid[int(food[0]/10)][int(food[1]/10)] = 3
        self.grid = self.grid.T
        for i in range(0, 30):
            for j in range(0, 30):
                if self.grid[i][j] == 1:
                    SH = [i, j]
                    break
        if scene_info['frame'] == 0:
            self.preFood = food
        
        checkPoint = [(0, 0), (290, 0), (290, 290), (0, 290)]

        command = "NONE"

        if self.state == 0:
            if snake_head[0] > food[0]:
                command = "LEFT"
            elif snake_head[0] < food[0]:
                command = "RIGHT"
            elif snake_head[1] > food[1]:
                command = "UP"
            elif snake_head[1] < food[1]:
                command = "DOWN"
            if food != self.preFood:
                self.preFood = food
                self.state = 1
        elif self.state >= 1:
            if snake_head[0] > checkPoint[self.state-1][0]:
                command = "LEFT"
            elif snake_head[0] < checkPoint[self.state-1][0]:
                command = "RIGHT"
            elif snake_head[1] > checkPoint[self.state-1][1]:
                command = "UP"
            elif snake_head[1] < checkPoint[self.state-1][1]:
                command = "DOWN"
            if snake_head == checkPoint[self.state-1]:
                self.state = self.state + 1
                if self.state >= 5:
                    command = "UP"
                    self.state = 0
                if snake_head[0] > checkPoint[self.state-1][0]:
                    command = "LEFT"
                elif snake_head[0] < checkPoint[self.state-1][0]:
                    command = "RIGHT"
                elif snake_head[1] > checkPoint[self.state-1][1]:
                    command = "UP"
                elif snake_head[1] < checkPoint[self.state-1][1]:
                    command = "DOWN"
                    
        if command == "LEFT" and self.dir == "RIGHT":
            command = "UP"
        if self.state == 1 and snake_head[1] == 0:
            command = "RIGHT"
            self.state = 2

        data = np.zeros((1, 5))
        data[0, 0] = int(snake_head[0])
        data[0, 1] = int(snake_head[1])
        data[0, 2] = int(food[0])
        data[0, 3] = int(food[0])
        if self.dir == "UP":
            data[0, 4] = 0
        if self.dir == "DOWN":
            data[0, 4] = 1
        if self.dir == "LEFT":
            data[0, 4] = 2
        if self.dir == "RIGHT":
            data[0, 4] = 3

        data = data[0, [0, 1, 2, 3, 4]].reshape(1, -1)   

        commandm = self.model.predict(data)

        if commandm == 0:
            commandm = "UP"
        if commandm == 1:
            commandm = "DOWN"
        if commandm == 2:
            commandm = "LEFT"
        if commandm == 3:
            commandm = "RIGHT"

        print(command, commandm)
        self.preDir = self.dir

        if self.dir == "DOWN":
            if (command != "DOWN" or command != "UP"):
                self.dir = command
        elif self.dir == "UP":
            if (command != "DOWN" or command != "UP"):
                self.dir = command
        elif self.dir == "RIGHT":
            if (command != "RIGHT" or command != "LEFT"):
                self.dir = command
        elif self.dir == "LEFT":
            if (command != "RIGHT" or command != "LEFT"):
                self.dir = command

        self.features.append([self.state, snake_head[0], snake_head[1], food[0], food[1], self.preDir, command])


        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
