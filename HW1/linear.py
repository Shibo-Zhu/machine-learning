import numpy as np


def getdata(dfpath, k=5):
    data = np.loadtxt(dfpath, delimiter=';', skiprows=1)
    # 给样本添加偏移量
    x_data = np.concatenate((data[:, :-1], np.ones((data.shape[0], 1))), axis=1)
    x_split_data = np.array_split(x_data, k)
    y_split_data = np.array_split(data[:, -1, np.newaxis], k)
    return x_split_data, y_split_data


def gettraindata(data):
    train = data.pop()
    for i in range(len(data)):
        train = np.append(train, data[1], axis=0)
    return train


class LinearRegression:
    def __init__(self, lam=0.2):
        self.lam = lam

    def getweights(self, xArr, yArr, lam=0.2):
        self.lam = lam
        xMat = np.mat(xArr)
        yMat = np.mat(yArr)

        xTx = xMat.T * xMat
        rxTx = xTx + np.eye(xMat.shape[1]) * self.lam
        self.weights = rxTx.I * xMat.T * yMat
        return self.weights

    def predict(self, X):
        return np.mat(X) * np.mat(self.weights)

    def MSE(self, y, truth):
        return np.sum((y - truth) ** 2) / len(y)


if __name__ == '__main__':
    red_file_path = '.\winequality-red.csv'
    white_file_path = '.\winequality-white.csv'
    # 获取数据
    k = 5
    r_xdata, r_ydata = getdata(red_file_path, k)
    w_xdata, w_ydata = getdata(white_file_path, k)

    # 初始化方差
    r_mse = w_mse = 0
    # 交叉验证
    for i in range(k):
        rmodel = LinearRegression()
        wmodel = LinearRegression()

        # copy data
        r_x = r_xdata.copy()
        r_y = r_ydata.copy()
        w_x = w_xdata.copy()
        w_y = w_ydata.copy()

        # distribute data
        r_xtest = r_x.pop(i)
        r_ytest = r_y.pop(i)
        r_xtrain = gettraindata(r_x)
        r_ytrain = gettraindata(r_y)
        w_xtest = w_x.pop(i)
        w_ytest = w_y.pop(i)
        w_xtrain = gettraindata(w_x)
        w_ytrain = gettraindata(w_y)

        rmodel.getweights(r_xtrain, r_ytrain)
        r_pred = rmodel.predict(r_xtest)
        r_mse += rmodel.MSE(np.array(r_pred), np.array(r_ytest))

        wmodel.getweights(w_xtrain, w_ytrain)
        w_pred = wmodel.predict(w_xtest)
        w_mse += wmodel.MSE(np.array(w_pred), np.array(w_ytest))

    print("redwine mse:", r_mse / k)
    print("whitewine mse:", w_mse / k)
