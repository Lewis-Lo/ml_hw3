import os 
import pickle
from snake import Snake

score = []

for i in range(0, 1578):

    sn = pickle.load(open("Snake_g1_{}.pickle".format(str(i+1)), "rb"))
    score.append(sn.score)

print(max(score))