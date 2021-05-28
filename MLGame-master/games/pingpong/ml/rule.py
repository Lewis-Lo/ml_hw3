"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.speed = 0
        self.preBall = [0, 0]

    def nextBall(self, scene_info, X, Y, direction, speed, side):
        # dir : 0:右上, 1:右下, 2:左上, 3:左下    
        tempX = X
        tempY = Y
        blockerL = scene_info['blocker'][0]
        blockerR = blockerL + 30
        blockerU = scene_info['blocker'][1]
        blockerD = blockerU + 20
        for i in range(0, speed):
            if(direction == 0):
                tempX = tempX + 1
                tempY = tempY - 1
            elif(direction == 1):
                tempX = tempX + 1
                tempY = tempY + 1
            elif(direction == 2):
                tempX = tempX - 1
                tempY = tempY - 1
            elif(direction == 3):
                tempX = tempX - 1
                tempY = tempY + 1

            # blocker
            if(tempX >= blockerL and tempX <= blockerR and tempY <= blockerU and tempY >= blockerD):
                # dir : 0:右上, 1:右下, 2:左上, 3:左下
                if(direction == 0):
                    if(tempX - blockerL >= blockerD - tempY):
                        return tempX, blockerD, 1
                    else:
                        return blockerL - 5, tempY, 2
                elif(direction == 1):
                    if(tempX - blockerL >= tempY - blockerU):
                        return tempX, blockerU - 5, 0
                    else:
                        return blockerL - 5, tempY, 3
                elif(direction == 2):
                    if(blockerR - tempX >= blockerD - tempY):
                        return tempX, blockerD, 3
                    else:
                        return blockerR, tempY, 0
                elif(direction == 3):
                    if(blockerR - tempX >= tempY - blockerU):
                        return tempX, blockerU - 5, 2
                    else:
                        return blockerR, tempY, 1

            # edge
            if(direction == 0):
                if(tempX >= 200):
                    return 195, tempY, 2
            elif(direction == 1):
                if(tempX >= 200):
                    return 195, tempY, 3
            elif(direction == 2):
                if(tempX <= 0):
                    return 0, tempY, 0 
            elif(direction == 3):
                if(tempX <= 0):
                    return 0, tempY, 1
            

        return tempX, tempY, direction

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info['ball_speed'])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            command = "NONE"

            speed = abs(scene_info['ball'][0] - self.preBall[0])
            X = scene_info['ball'][0]
            Y = scene_info['ball'][1]

            # dir : 0:右上, 1:右下, 2:左上, 3:左下
            direction = 0
            deltaBall = [0, 0]
            deltaBall[0] = scene_info['ball'][0] - self.preBall[0]
            deltaBall[1] = scene_info['ball'][1] - self.preBall[1]
            if(deltaBall[0] > 0 and deltaBall[1] < 0):
                direction = 0
            elif(deltaBall[0] > 0 and deltaBall[1] > 0):
                direction = 1
            elif(deltaBall[0] < 0 and deltaBall[1] < 0):
                direction = 2
            elif(deltaBall[0] < 0 and deltaBall[1] > 0):
                direction = 3

            for i in range(0, 200):
                if(Y >= 420 or Y <= 80):
                    break
                X, Y, direction = self.nextBall(scene_info, X, Y, direction, speed, self.side)
                
            X2 = X
            Y2 = Y
            direction2 = direction
            if(Y >= 420):
                if(direction == 1):
                    direction2 = 0
                elif(direction == 3):
                    direction2 = 2
            elif(Y <= 80):
                if(direction == 0):
                    direction2 = 1
                elif(direction == 2):
                    direction2 = 3
            X2, Y2, direction2 = self.nextBall(scene_info, X2, Y2, direction2, speed, self.side)
            X2, Y2, direction2 = self.nextBall(scene_info, X2, Y2, direction2, speed, self.side)
            # dir : 0:右上, 1:右下, 2:左上, 3:左下   
            for i in range(0, 200):
                if(Y2 >= 420 or Y2 <= 80):
                    break
                X2, Y2, direction2 = self.nextBall(scene_info, X2, Y2, direction2, speed, self.side)

            if(self.side == '1P'):
                if(direction == 1 or direction == 3):
                    if((scene_info['platform_1P'][0] + 20 - X) >= 7):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_1P'][0] + 20 - X) <= -7):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                else:
                    if((scene_info['platform_1P'][0] + 20 - X2) >= 7):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_1P'][0] + 20 - X2) <= -7):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'

            elif(self.side == '2P'):
                if(direction == 0 or direction == 2):
                    if((scene_info['platform_2P'][0] + 20 - X) >= 7):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_2P'][0] + 20 - X) <= -7):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                else:
                    if((scene_info['platform_2P'][0] + 20 - X2) >= 7):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_2P'][0] + 20 - X2) <= -7):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'

            # print(scene_info['ball'])
            # print(X)
            # print(self.side)
            # print(command)
            predict = [X, Y]
            predict2 = [X2, Y2]
            plat = [scene_info["platform_1P"][0], scene_info["platform_2P"][0]]
            print("[{},{},{}]".format(predict, plat, scene_info['ball']))
            self.preBall = scene_info['ball']
            
            
            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
