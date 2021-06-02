"""
The template of the script for playing the game in the ml mode
"""
from newGen import newGen
import pickle
from snake_v3 import Snake
import numpy as np
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.grid = np.zeros((30, 30))
        self.dir = "abDOWN"
        self.s = pickle.load(open("Snake_g3_72_v3.pickle", "rb"))
        self.sList = []
        self.generation = 0
        self.snakeIndex = 0
        self.tgrid = np.zeros((30, 30)) 
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            
            self.s.fitness = 0
            self.s.score = 0
            self.s.cc = [0, 0, 0]
            self.s.leftStep = 300



            self.dir = "abDOWN"
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

        if(scene_info['frame'] == 0):
            self.preFoodPos = [int(food[0]/10), int(food[1]/10)]
        if(self.preFoodPos != [int(food[0]/10), int(food[1]/10)]):
            self.preFoodPos = [int(food[0]/10), int(food[1]/10)]
            self.s.getApple()
        
        command = self.s.move(self.s.sensor(self.grid, self.dir), self.dir)

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

        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
