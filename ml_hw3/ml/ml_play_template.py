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
        self.s = Snake()# pickle.load(open("Snake_g1_45.pickle", "rb"))
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
            self.tgrid = np.zeros((30, 30)) 
            count = 0
            fit = self.s.fitness
            print(self.s.cc)
            for j in range(0, 3):
                if self.s.cc[j] <= 5 :
                    count = count + 1

            if count == 0:
                fit = self.s.fitness * 10
            elif count == 2:
                fit = 0
            if(self.s.score < 10) :
                fit = (fit ** 2) * pow(2,self.s.score)
            else :
                fit = (fit ** 2) * pow(2,10) * (self.s.score-9) * pow(2,self.s.score)
            print("SnakeFitness:", fit)
            self.snakeIndex = self.snakeIndex + 1
            if self.snakeIndex > 1000:
                self.generation = self.generation + 1
                self.snakeIndex = 1
                newGen(self.sList, self.generation)
                self.sList.clear()

            if(self.generation == 0):
                self.generation = 1
                self.snakeIndex = 1
            self.s = pickle.load(open("Snake_g{}_{}_v3.pickle".format(self.generation, self.snakeIndex), "rb"))
            self.sList.append(self.s)
            self.s.fitness = 0
            self.s.score = 0
            self.s.cc = [0, 0, 0]
            self.s.leftStep = 300
            print("Generation:{} Snake:{}".format(self.generation, self.snakeIndex))


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
