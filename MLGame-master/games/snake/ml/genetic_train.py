"""
The template of the script for playing the game in the ml mode
"""
from snake import Snake
import numpy as np
import pickle
import generation
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.grid = np.zeros((30, 30))
        self.s1 = Snake()
        self.preFoodPos = [0, 0]
        self.index = 0
        self.round = 9
        self.generation = 2
        self.snakes = []
        pass

    def nextGen(self):
        self.generation = self.generation + 1
        self.index = 1
        score = []
        rank = []
        for i in range(0, 200):
            score = self.snakes[i].getAvgScore()

        rk1 = 0
        for i in range(1, 200):
            if(score[i] > score[rk1]):
                rk1 = i
        rank.append(self.snakes[rk1])
        self.snakes.remove(self.snakes[rk1])

        rk2 = 0
        for i in range(1, 199):
            if(score[i] > score[rk2]):
                rk2 = i
        rank.append(self.snakes[rk2])
        self.snakes.remove(self.snakes[rk2])

        rk3 = 0
        for i in range(1, 198):
            if(score[i] > score[rk3]):
                rk3 = i
        rank.append(self.snakes[rk3])
        self.snakes.remove(self.snakes[rk3])

        rk4 = 0
        for i in range(1, 197):
            if(score[i] > score[rk4]):
                rk4 = i
        rank.append(self.snakes[rk4])
        self.snakes.remove(self.snakes[rk4])

        self.snakes.clear()

        newGen = generation.newGen(rk1, rk2, rk3, rk4)

        for i in range(0, 200):
            pickle.dump(newGen[i], open("Snake_g{}_{}.pickle".format(str(self.generation), str(i + 1)),"wb"))

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            self.round = self.round + 1
            self.s1.remake()
            if self.round >= 10:
                self.round = 0
                self.index = self.index + 1
                if(self.index > 200):
                    self.nextGen()

                self.s1 = pickle.load(open("Snake_g{}_{}.pickle".format(str(self.generation), str(self.index)), "rb"))
                print("now: generation {} snake {}".format(str(self.generation), str(self.index)))
                self.snakes.append(self.s1)

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
            self.s1.getApple()
        
        command = self.s1.move(self.s1.sensor(self.grid))

        return command
    def reset(self):
        """
        Reset the status if needed
        """
        pass
