import numpy as np
class Snake:
    def __init__(self):
        pass

    def move(self, grid, hdir):
        sight = self.sensor(grid)
        command = "NONE"

        if hdir == "abUP":
            if sight[0] == 2 and sight[3] != 1:
                command = "RIGHT"
            elif sight[0] == 1 and sight[3] == 1:
                command = "LEFT"
            
        elif hdir == "abRIGHT":
            if sight[0] == 2:
                command = "DOWN"
            elif sight[1] == 1:
                command = "UP"

        elif hdir == "abLEFT":
            if sight[2] == 1:
                command = "DOWN"

        elif hdir == "abDOWN":
            if sight[1] == 1:
                command = "RIGHT"

        print(hdir, sight, command)
                
        return command
        

    def sensor(self, grid):
        output = np.zeros(4)
        snakeHead = [0, 0]
        for i in range(0, 30):
            for j in range(0, 30):
                if grid[i][j] == 1:
                    snakeHead[0] = i
                    snakeHead[1] = j

        output[0] = snakeHead[0] + 1    # UP
        output[1] = 30 - snakeHead[0]   # DOWN
        output[2] = snakeHead[1] + 1    # LEFT
        output[3] = 30 - snakeHead[1]   # RIGHT

        return output