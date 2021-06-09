"""
The template of the script for playing the game in the ml mode
"""
from newGen import newGen
import pickle
from snakeMacro import SnakeMacro
import numpy as np
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.grid = np.zeros((30, 30))
        self.dir = "abDOWN"
        self.l = []
        self.l.append(pickle.load(open("Snake_g5_376_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_300_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_331_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_579_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_668_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_868_v3.pickle", "rb")))
        self.l.append(pickle.load(open("Snake_g5_905_v3.pickle", "rb")))
        self.s = SnakeMacro(self.l)
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
            self.s.leftStep = 1000
            self.s.loopCount = 200
  

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
        
        command = self.s.move(self.grid, self.dir)

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
