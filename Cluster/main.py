import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt


def dis(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


data = pd.read_csv('dataset.csv')
columns = data.columns
targetList = ['BHMBCCMKT01', 'BHMMBMMBX01', 'BHMNCPHST01', 'BHMNCPNST01', 'BHMBCCTHL01']
newdata = data[data[columns[0]].isin(targetList)].copy()
C = np.zeros(newdata.shape[0])

# 时间，化为秒
t = []
for i in range(newdata.shape[0]):
    h = int(newdata[columns[3]].iloc[i][11:13])
    m = int(newdata[columns[3]].iloc[i][14:16])
    s = int(newdata[columns[3]].iloc[i][-2:])
    if h < 8:
        t.append(0)
    else:
        _t = (h - 8) * 60 * 60 + m * 60 + s
        t.append(_t)

K = 5
CentPoints = []
for i in range(K):
    cer = random.randint(0, newdata.shape[0] - 1)
    # print(cer)
    CentPoints.append([newdata[columns[2]].iloc[cer], t[cer]])
# print(CentPoint)

for p in range(10):
    NewPoint = [[0, 0] for i in range(K)]
    for i in range(newdata.shape[0]):
        mdis = 1e9
        mC = 0
        for j in range(len(CentPoints)):
            centpoint = CentPoints[j]
            distance = dis((newdata[columns[2]].iloc[i], t[i]), centpoint)
            if mdis > distance:
                mdis = distance
                mc = j
        C[i] = mc
        NewPoint[mc][0] += newdata[columns[2]].iloc[i]
        NewPoint[mc][1] += t[i]

    for i in range(K):
        CentPoints[i][0] = NewPoint[i][0] / newdata.shape[0]
        CentPoints[i][1] = NewPoint[i][1] / newdata.shape[0]

for i in range(newdata.shape[0]):
    if C[i] == 0:
        plt.plot(newdata[columns[2]].iloc[i], t[i], 'r.')
    elif C[i] == 1:
        plt.plot(newdata[columns[2]].iloc[i], t[i], 'g.')
    elif C[i] == 2:
        plt.plot(newdata[columns[2]].iloc[i], t[i], 'b.')
    elif C[i] == 3:
        plt.plot(newdata[columns[2]].iloc[i], t[i], color='pink', marker='.')
    elif C[i] == 4:
        plt.plot(newdata[columns[2]].iloc[i], t[i], color='orange', marker='.')
plt.show()
