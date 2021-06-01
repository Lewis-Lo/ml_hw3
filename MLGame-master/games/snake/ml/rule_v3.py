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
        self.snakeIndex = 0
        self.tgrid = np.zeros((30, 30)) 
        self.preFood = [0, 0]
        self.dir = "DOWN"
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            # self.tgrid = np.zeros((30, 30)) 
            # print("SnakeScore:", self.s.score)
            # self.snakeIndex = self.snakeIndex + 1
            # if self.snakeIndex > 2000:
            #     self.generation = self.generation + 1
            #     self.snakeIndex = 1
            #     newGen(self.sList, self.generation)
            #     self.sList.clear()

            # if(self.generation == 0):
            #     self.generation = 1
            #     self.snakeIndex = 1
            # self.s = pickle.load(open("Snake_g{}_{}.pickle".format(self.generation, self.snakeIndex), "rb"))
            # self.sList.append(self.s)
            # self.s.score = 0
            # print("Generation:{} Snake:{}".format(self.generation, self.snakeIndex))

            self.state = 1
            self.dir = "DOWN"
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

        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
