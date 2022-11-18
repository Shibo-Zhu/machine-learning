import torch
import math
import matplotlib.pyplot as plt


def dis(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


X = torch.randn(2000) * 100
y = torch.randn(2000) * 100
C = torch.zeros(2000)

K = 5
CentPoint = []

for i in range(K):
    CentPoint.append([torch.randint(-100, 100, (1,)).item(),
                      torch.randint(-100, 100, (1,)).item()])

print(CentPoint)
for p in range(10):
    NewPoint = [[0, 0] for i in range(K)]
    for i in range(len(X)):
        mDis = 1e9
        mC = 0
        for j in range(len(CentPoint)):
            cp = CentPoint[j]
            D = dis([X[i].item(), y[i].item()], cp)
            if mDis > D:
                mDis = D
                mC = j
        C[i] = mC
        NewPoint[mC][0] += X[i].item()
        NewPoint[mC][1] += y[i].item()

    for i in range(K):
        CentPoint[i][0] = NewPoint[i][0] / 2000
        CentPoint[i][1] = NewPoint[i][1] / 2000
    print(CentPoint)

cc = list(C)
for i in range(len(X)):
    if cc[i] == 0:
        plt.plot(X[i].item(), y[i].item(), 'r.')
    elif cc[i] == 1:
        plt.plot(X[i].item(), y[i].item(), 'g.')
    elif cc[i] == 2:
        plt.plot(X[i].item(), y[i].item(), 'b.')
    elif cc[i] == 3:
        plt.plot(X[i].item(), y[i].item(), color='pink', marker='.')
    elif cc[i] == 4:
        plt.plot(X[i].item(), y[i].item(), color='orange', marker='.')

for CP in CentPoint:
    plt.plot(CP[0], CP[1], color='black', marker='X')

plt.show()