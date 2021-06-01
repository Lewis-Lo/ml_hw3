"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.start = 1
        self.eat = 0
        self.prefood = [0, 0]
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        snake_head = scene_info["snake_head"]
        food = scene_info["food"]

        check = [0, 0]
        if(self.prefood[0]<=150 and self.prefood[1]<=150):
            check = [250, 250]
        elif(self.prefood[0]>150 and self.prefood[1]<=150):
            check = [50, 250]
        elif(self.prefood[0]>150 and self.prefood[1]>150):
            check = [50,50]
        elif(self.prefood[0]<=150 and self.prefood[1]>150):
            check = [250, 50]

        if scene_info['frame'] == 0:
            self.prefood = food

        if self.prefood != food:
            self.prefood = food
            self.eat = 0
            self.start = 1

        if snake_head[0] == check[0] and snake_head[1] == check[1]:
            self.start = 0
            self.eat = 1

        command = 0

        if self.start == 1:
            if snake_head[0] > check[0]:
                command = "LEFT"
            elif snake_head[0] < check[0]:
                command = "RIGHT"
            elif snake_head[1] > check[1]:
                command = "UP"
            elif snake_head[1] < check[1]:
                command = "DOWN"
        else:
            if snake_head[0] > food[0]:
                command = "LEFT"
            elif snake_head[0] < food[0]:
                command = "RIGHT"
            elif snake_head[1] > food[1]:
                command = "UP"
            elif snake_head[1] < food[1]:
                command = "DOWN"
        print(command)
        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass
