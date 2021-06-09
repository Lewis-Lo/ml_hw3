"""
The template of the script for playing the game in the ml mode
"""
import numpy as np
from snake import Snake
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.dir = "abDOWN"
        self.predir = "abDOWN"
        self.grid = np.zeros((30, 30))
        self.log = []
        self.logIndex = 1
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            pickle.dump(self.log, open("log_{}.pickle".format(self.logIndex), "wb"))
            self.dir = "abDOWN"
            self.predir = "abDOWN"
            self.grid = np.zeros((30, 30))
            self.log = []
            self.logIndex = self.logIndex + 1
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

        s = Snake()
        command = s.move(self.grid, self.dir)

        self.predir = self.dir

        td = self.dir

        if self.dir == "abDOWN":
            if(command != "DOWN" or command != "UP"):
                self.dir = "ab"+command
        elif self.dir == "abUP":
            if(command != "DOWN" or command != "UP"):
                self.dir = "ab"+command
        elif self.dir == "abRIGHT":
            if(command != "RIGHT" or command != "LEFT"):
                self.dir = "ab"+command
        elif self.dir == "abLEFT":
            if(command != "LEFT" or command != "RIGHT"):
                self.dir = "ab"+command

        if command == "NONE":
            self.dir = td

        if len(snake_body) >= 300:
            command = "NONE"
        
        logf = [s.sensor(self.grid), self.predir, command]
        self.log.append(logf)

        return command



    def reset(self):
        """
        Reset the status if needed
        """
        pass
