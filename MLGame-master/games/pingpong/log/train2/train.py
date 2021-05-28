import pickle
import os 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble, preprocessing, metrics
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz

files = ['', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '']

for index in range(0, 345):
    files[index] = ("features{}.pickle".format(str(index+1)))

data = pickle.load(open(files[0], 'rb'))

for index in files[0:345]:
    temp = pickle.load(open(index, 'rb'))
    data = np.hstack((data, temp))

data = data.T
dataXP1 = data[:, [0, 1, 2, 3, 4, 6, 7, 8]]
dataXP2 = data[:, [0, 1, 2, 3, 5, 6, 7, 8]]
dataYP1 = data[:, 9]
dataYP2 = data[:, 10]

X_trainP1, X_testP1, Y_trainP1, Y_testP1 = train_test_split(dataXP1, dataYP1, test_size = 0.3)
X_trainP2, X_testP2, Y_trainP2, Y_testP2 = train_test_split(dataXP2, dataYP2, test_size = 0.3)

dtc = tree = DecisionTreeClassifier(criterion = 'entropy', max_depth=100, random_state=5)
dtc.fit(X_trainP1, Y_trainP1)
print(dtc.score(X_testP1, Y_testP1))
pickle.dump(dtc, open('dtcP1_v2.pickle', 'wb'))

dtc = tree = DecisionTreeClassifier(criterion = 'entropy', max_depth=100, random_state=5)
dtc.fit(X_trainP2, Y_trainP2)
print(dtc.score(X_testP2, Y_testP2))
pickle.dump(dtc, open('dtcP2_v2.pickle', 'wb'))

plt.figure(figsize=(8, 8))  # 設定新圖表大小
plt.rcParams['font.size'] = 14  # 設定圖表字體大小
plt.title('Original data')  # 圖表標題
# 將資料繪成散佈圖 (根據標籤分顏色)
plt.scatter(dataXP1.T, dataYP1.T)
plt.grid(True)  # 繪製格線
# 設定 X 與 Y 軸顯示範圍
plt.xlim([np.amin(dataXP1.T[0]), np.amax(dataXP1.T[0])])
plt.ylim([np.amin(dataXP1.T[1]), np.amax(dataXP1.T[1])])
plt.tight_layout()  # 減少圖表的白邊
plt.show()  # 顯示圖表

