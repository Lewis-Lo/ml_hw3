import pickle
from snake_v3 import Snake

for i in range(0, 1000):
    s = Snake()
    pickle.dump(s, open("Snake_g1_{}_v3.pickle".format(i+1), "wb"))
