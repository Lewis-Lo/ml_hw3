from snake_vm import Snake
import pickle
class SnakeMacro:
    def __init__(self, snakeList):
        self.brains = snakeList
        self.Score = 0
        self.leftStep = 1000
        self.brainIndex = 0
        self.brainNum = len(snakeList)
        self.loopCount = 200

    def move(self, grid, hdir):
        for i in range(0, self.brainNum):
            self.brains[i].leftStep = 1000
            self.brains[i].loop = 0
        self.leftStep = self.leftStep - 1
        if self.leftStep <= 0:
            return "NONE"
        self.loopCount = self.loopCount - 1
        if self.loopCount <= 0:
            self.loopCount = 200
            self.brainIndex = (self.brainIndex + 1) % self.brainNum
        return self.brains[self.brainIndex].move(self.brains[self.brainIndex].sensor(grid, hdir), hdir)

    def getApple(self):
        self.leftStep = self.leftStep + 300
        self.loopCount = 200
        self.brainIndex = (self.brainIndex + 1) % self.brainNum
        self.Score = self.Score + 1