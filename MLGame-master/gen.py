import generation
import pickle

rk1 = pickle.load(open("Snake_g1_s20.pickle", "rb"))
rk2 = pickle.load(open("Snake_g1_s7.pickle", "rb"))
rk3 = pickle.load(open("Snake_g1_s9.pickle", "rb"))
rk4 = pickle.load(open("Snake_g1_s13.pickle", "rb"))

newGen = generation.newGen(rk1, rk2, rk3, rk4)

for i in range(0, 200):
    pickle.dump(newGen[i], open("Snake_g2_{}.pickle".format(str(i + 1)),"wb"))

# print(rk1.L4_weight)
# print(newGen[0].L4_weight)