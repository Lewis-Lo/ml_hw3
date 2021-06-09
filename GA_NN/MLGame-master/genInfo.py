import numpy as np
import pickle
class geninfo:
    def __init__(self):
        self.gen = 0
        self.score = []
        self.fitness = []
    
    def avgScore(self):
        return np.mean(self.score)

    def avgFitness(self):
        return np.mean(self.fitness)
        
    def avgScoreRank(self, rank):
        temp = sorted(self.score)
        return np.mean(np.mean(temp[0:rank]))

    def dumpGeninfo(self):
        pickle.dump(self, open("GenInfo_{}.pickle".format(self.gen), "wb"))

    def loadGeninfo(self):
        self = pickle.load(open("GenInfo_{}.pickle".format(self.gen), "rb"))