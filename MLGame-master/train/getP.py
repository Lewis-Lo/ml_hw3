import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier

mlp = pickle.load(open("mlp.pickle", "rb"))
# MLPClassifier.intercepts_
# print(mlp.coefs_)
# print(mlp.intercepts_)
print(mlp.get_params())