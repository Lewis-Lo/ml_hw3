"""
The template of the script for playing the game in the ml mode
"""
from snake import Snake
import numpy as np
import pickle
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.grid = np.zeros((30, 30))
        self.s1 = Snake()
        self.preFoodPos = [0, 0]
        self.index = 0
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            if(self.s1.getScore() >= 0.27):
                self.index = self.index + 1
                # pickle.dump(self.s1, open("Snake_g1_{}.pickle".format(self.index), 'wb'))
            print("Snake_Score{}".format(self.s1.getScore()))
            self.s1 = Snake()
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
