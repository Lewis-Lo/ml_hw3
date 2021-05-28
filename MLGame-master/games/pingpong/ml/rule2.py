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
        self.preBlocker = 0
        self.tempBlocker = 0

    def nextBall(self, scene_info, X, Y, direction, speed, side):
        # dir : 0:右上, 1:右下, 2:左上, 3:左下    
        tempX = X
        tempY = Y
        blockerL = self.tempBlocker# scene_info['blocker'][0] # self.tempBlocker
        blockerR = blockerL + 30
        blockerU = scene_info['blocker'][1]
        blockerD = blockerU + 20
    
        if(direction == 0):
            tempX = tempX + abs(scene_info['ball_speed'][0])
            tempY = tempY - abs(scene_info['ball_speed'][1])
        elif(direction == 1):
            tempX = tempX + abs(scene_info['ball_speed'][0])
            tempY = tempY + abs(scene_info['ball_speed'][1])
        elif(direction == 2):
            tempX = tempX - abs(scene_info['ball_speed'][0])
            tempY = tempY - abs(scene_info['ball_speed'][1])
        elif(direction == 3):
            tempX = tempX - abs(scene_info['ball_speed'][0])
            tempY = tempY + abs(scene_info['ball_speed'][1])

        # blocker
        if(((tempX + 5) >= blockerL or tempX >= blockerL) and tempX <= blockerR and ((tempY + 5) >= blockerU or tempY >= blockerU) and tempY <= blockerD):
            # dir : 0:右上, 1:右下, 2:左上, 3:左下
            '''
            if(direction == 0):
                if(Y >= blockerD and X >=blockerL):
                    return tempX, blockerD, 1
                else:
                    return blockerL - 5, tempY, 2
            elif(direction == 1):
                if((Y+5) <= blockerU and X >= blockerL):
                    return tempX, blockerU - 5, 0
                else:
                    return blockerL - 5, tempY, 3
            elif(direction == 2):
                if(Y >= blockerD and (X+5) <= blockerR):
                    return tempX, blockerD, 3
                else:
                    return blockerR, tempY, 0
            elif(direction == 3):
                if((Y+5) <= blockerU and (X+5) <= blockerR):
                    return tempX, blockerU - 5, 2
                else:
                    return blockerR, tempY, 1
            '''
            if(direction == 0):
                if(abs(tempX - blockerL) > abs(tempY - blockerD)):
                    return tempX, blockerD, 1
                else:
                    return blockerL - 5, tempY, 2
            elif(direction == 1):
                if(abs(tempX - blockerL) > abs(tempY - blockerU)):
                    return tempX, blockerU - 5, 0
                else:
                    return blockerL - 5, tempY, 3
            elif(direction == 2):
                if(abs(tempX - blockerR) > abs(tempY - blockerD)):
                    return tempX, blockerD, 3
                else:
                    return blockerR, tempY, 0
            elif(direction == 3):
                if(abs(tempX - blockerR) > abs(tempY - blockerU)):
                    return tempX, blockerU - 5, 2
                else:
                    return blockerR, tempY, 1
            

        # edge
        if(direction == 0):
            if(tempX > 195):
                return 195, tempY, 2
        elif(direction == 1):
            if(tempX > 195):
                return 195, tempY, 3
        elif(direction == 2):
            if(tempX < 0):
                return 0, tempY, 0 
        elif(direction == 3):
            if(tempX < 0):
                return 0, tempY, 1
            

        return tempX, tempY, direction

    def tempBlockerC(self, d):
        temp = self.tempBlocker
        temp = temp + 5*d
        if(temp > 170):
            temp = 165
            d = -1
        elif(temp < 0):
            temp = 5
            d = 1
        self.tempBlocker = temp
        return d

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

            speed = abs(scene_info['ball_speed'][0])
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
            direc = direction

            blockerD = 1
            if(scene_info['blocker'][0] - self.preBlocker > 0):
                blockerD = 1    # right
            elif(scene_info['blocker'][0] - self.preBlocker < 0):
                blockerD = -1    #left
            self.tempBlocker = scene_info['blocker'][0]

            nextSide = 0
            for i in range(0, 200):
                if(Y >= 420):
                    nextSide = 1
                    break
                elif(Y <= 80):
                    nextSide = 2
                    break
                X, Y, direction = self.nextBall(scene_info, X, Y, direction, speed, self.side)

                blockerD = self.tempBlockerC(blockerD)
                # self.tempBlocker = self.tempBlocker + blockerD * 5
                # if(self.tempBlocker > 170):
                #     self.tempBlocker = self.tempBlocker - 10
                #     blockerD = blockerD * -1
                # elif(self.tempBlocker < 0):
                #     self.tempBlocker = self.tempBlocker + 10
                #     blockerD = blockerD * -1
                
                

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
            next2Side = 0   
            for i in range(0, 200):
                if(Y2 >= 420):
                    next2Side = 1
                    break
                elif(Y2 <= 80):
                    next2Side = 2
                    break
                X2, Y2, direction2 = self.nextBall(scene_info, X2, Y2, direction2, speed, self.side)
                if(self.tempBlocker > 170):
                    self.tempBlocker = self.tempBlocker - 10
                    blockerD = blockerD * -1
                elif(self.tempBlocker < 0):
                    self.tempBlocker = self.tempBlocker + 10
                    blockerD = blockerD * -1

            if(self.side == '1P'):
                if(nextSide == 1):
                    if((scene_info['platform_1P'][0] + 20 - X) >= 6):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_1P'][0] + 20 - X) <= -6):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                elif(next2Side == 1):
                    if((scene_info['platform_1P'][0] + 20 - X2) >= 6):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_1P'][0] + 20 - X2) <= -6):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                else:
                    if((scene_info['platform_1P'][0] + 20 - 100) >= 6):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_1P'][0] + 20 - 100) <= -6):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'

            elif(self.side == '2P'):
                if(nextSide == 2):
                    if((scene_info['platform_2P'][0] + 20 - X) >= 6):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_2P'][0] + 20 - X) <= -6):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                # elif(next2Side == 2):
                #     if((scene_info['platform_2P'][0] + 20 - X2) >= 6):
                #         command = 'MOVE_LEFT'
                #     elif((scene_info['platform_2P'][0] + 20 - X2) <= -6):
                #         command = 'MOVE_RIGHT'
                #     else:
                #         command = 'NONE'
                else:
                    if((scene_info['platform_2P'][0] + 20 - 100) >= 6):
                        command = 'MOVE_LEFT'
                    elif((scene_info['platform_2P'][0] + 20 - 100) <= -6):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'

            predict = [X, Y]
            plat = [scene_info["platform_1P"][0], scene_info["platform_2P"][0]]
            # if(self.side == '1P'):
            #     print("[{},{},{},{}]".format(predict, plat, scene_info['ball'], direc))
            #     print(self.tempBlocker, scene_info['blocker'][0])
            self.preBall = scene_info['ball']
            self.preBlocker = scene_info['blocker'][0]

            
            
            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
