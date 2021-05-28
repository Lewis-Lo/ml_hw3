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
        pass

    def UP_DOWN(self, head):
        if(head[1] == 0):
            return "DOWN"
        if(head[1] == 29):
            return "UP"
        up = 0
        down = 0
        for i in range(0, head[0]):
            for j in range(0, 30):
                if(self.grid[i][j] == 2 or self.grid[i][j] == 4):
                    up = up + 1
        for i in range(head[0] + 1, 30):
            for j in range(0, 30):
                if(self.grid[i][j] == 2 or self.grid[i][j] == 4):
                    down = down + 1
        if up >= down:
            return "DOWN"
        return "UP"

    def RIGHT_LEFT(self, head):
        if(head[0] == 0):
            return "RIGHT"
        if(head[0] == 29):
            return "LEFT"
        right = 0
        left = 0
        for i in range(0, head[1]):
            for j in range(0, 30):
                if(self.grid[j][i] == 2 or self.grid[j][i] == 4):
                    left = left + 1
        for i in range(head[1] + 1, 30):
            for j in range(0, 30):
                if(self.grid[j][i] == 2 or self.grid[j][i] == 4):
                    right = right + 1
        if left >= right:
            return "RIGHT"
        return "LEFT"

    def circle(self, command):
        tempGrid = np.copy(self.grid)
        temptempGrid = np.copy(tempGrid)
        flag = 0
        for i in range(0, 30):
            for j in range(0, 30):
                temptempGrid = np.copy(self.grid)
                if(tempGrid[j][i] == 0):
                    tempGrid[j][i] = int(self.ext(j, i, temptempGrid))
                    if(tempGrid[j][i] == -1):
                        flag = 1
                
        
    def ext(self, x, y, Grid):
        if(x <= 0 or x >= 29 or y <= 0 or y >= 29):
            return 0
        Grid[y][x] = 100
        if(Grid[y-1][x] == 0):
            return self.ext(x, y-1, Grid)
        if(Grid[y][x-1] == 0):
            return self.ext(x-1, y, Grid)
        if(Grid[y+1][x] == 0):
            return self.ext(x, y+1, Grid)
        if(Grid[y][x+1] == 0):
            return self.ext(x+1, y, Grid)
        return -1

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
        # print(self.grid)
        command = "UP"

        headx = int(snake_head[0]/10)
        heady = int(snake_head[1]/10)
        foodx = int(food[0]/10)
        foody = int(food[1]/10)

        if headx > foodx:
            command =  "LEFT"
            if(self.direction == "RIGHT"):
                command = self.UP_DOWN((heady, headx))
        elif headx < foodx:
            command =  "RIGHT"
            if(self.direction == "LEFT"):
                command = self.UP_DOWN((heady, headx))
        elif heady > foody:
            command =  "UP"
            if(self.direction == "DOWN"):
                command = self.RIGHT_LEFT((heady, headx))
        elif heady < foody:
            command =  "DOWN"
            if(self.direction == "UP"):
                command = self.RIGHT_LEFT((heady, headx))
        
        if(command == "LEFT"):
            if(headx-1>=0):
                if(self.grid[heady][headx-1] == 2 or self.grid[heady][headx-1] == 4):
                    command = self.UP_DOWN((heady, headx))
            else:
                command = self.UP_DOWN((heady, headx))
        if(command == "RIGHT"):
            if(headx+1<30):
                if(self.grid[heady][headx+1] == 2 or self.grid[heady][headx+1] == 4):
                    command = self.UP_DOWN((heady, headx))
            else:
                command = self.UP_DOWN((heady, headx))
        if(command == "UP"):
            if(heady-1>=0):
                if(self.grid[heady-1][headx] == 2 or self.grid[heady-1][headx] == 4):
                    command = self.RIGHT_LEFT((heady, headx))
            else:
                command = self.RIGHT_LEFT((heady, headx))
        if(command == "DOWN"):
            if(heady+1<30):
                if(self.grid[heady+1][headx] == 2 or self.grid[heady+1][headx] == 4):
                    command = self.RIGHT_LEFT((heady, headx))
            else:
                command = self.RIGHT_LEFT((heady, headx))
                           
        if(self.grid[0][0] == 1):
            if(self.direction == "UP"):
                command = "RIGHT"
            else :
                command = "DOWN"
        if(self.grid[0][29] == 1):
            if(self.direction == "RIGHT"):
                command = "DOWN"
            else :
                command = "LEFT"
        if(self.grid[29][0] == 1):
            if(self.direction == "LEFT"):
                command = "UP"
            else :
                command = "RIGHT"
        if(self.grid[29][29] == 1):
            if(self.direction == "RIGHT"):
                command = "UP"
            else :
                command = "LEFT"

        self.circle(command)

        self.direction = command
        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
