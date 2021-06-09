import pickle
import matplotlib.pyplot as plt
import numpy as np

avgscore = []
topscore = []
gen = []
for i in range(1, 24):
    info = pickle.load(open("GenInfo_{}.pickle".format(i), "rb"))
    gen.append(i)
    avgscore.append(info.avgScore())
    temp = sorted(info.score)
    temp = np.mean(np.mean(temp[990:1000]))
    topscore.append(temp)

plt.plot(gen, avgscore)
plt.plot(gen, topscore)
plt.xlabel("Generation")
plt.ylabel("Score")
plt.legend(("avg score of 1000 snakes", "top 10 score of 1000 snakes"))
plt.show()