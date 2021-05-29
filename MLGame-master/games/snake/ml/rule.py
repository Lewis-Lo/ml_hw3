"""
The template of the script for playing the game in the ml mode
"""
import numpy as np

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.direction = "UP"
        self.grid = np.zeros((30, 30))
        self.openlist = []
        self.closelist = []
        pass

    def A_star_H(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def A_star_F(self, a, b):
        return 1 + self.A_star_H(a, b)

    def search_path(self, a, b):
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        snake_head = scene_info["snake_head"]
        snake_body = scene_info["snake_body"]
        food = scene_info["food"]

        self.grid = np.zeros((30, 30))
        # 0:empty
        # 1:head
        # 2:body
        # 3:food
        # 4:tail

        self.grid[int(snake_head[0]/10)][int(snake_head[1]/10)] = 1
        for i in snake_body:
            self.grid[int(i[0]/10)][int(i[1]/10)] = 2
        self.grid[int(food[0]/10)][int(food[1]/10)] = 3
        self.grid[int(snake_body[-1][0]/10)][int(snake_body[-1][1]/10)] = 4
        self.grid = self.grid.T
        print(self.grid)
        command = "UP"

        if snake_head[0] > food[0]:
            command =  "LEFT"
        elif snake_head[0] < food[0]:
            command =  "RIGHT"
        elif snake_head[1] > food[1]:
            command =  "UP"
        elif snake_head[1] < food[1]:
            command =  "DOWN"

        
        self.direction = command
        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
