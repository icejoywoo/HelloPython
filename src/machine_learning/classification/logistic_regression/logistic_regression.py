#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-2-19
# http://my.oschina.net/zenglingfan/blog/177586

from math import *


# 加载数据, 前两列是点所属的 X1, X2 坐标, 最后一列是该点所属分类
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        # 因为线性回归化式为 H(x) = W0 + W1*X1 + W2*X2
        # 即为 (W0, W1, W2)*(1, X1, X2), 其中 (W0, W1, W2) 即为所求回归系数 W
        # 为了方便计算, 读出 X1, X2 后要在前面补上一个 1.0
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


# sigmoid 函数
def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


# 梯度上升算法计算出最佳回归系数
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)  # convert to NumPy matrix
    labelMat = mat(classLabels).transpose()  # convert to NumPy matrix
    m, n = shape(dataMatrix)
    print m, n, dataMatrix
    alpha = 0.001  # 步长
    maxCycles = 500  # 循环次数
    weights = ones((n, 1))  # 回归系数初始化为 1

    # 循环 maxCycles 次, 每次都沿梯度向真实值 labelMat 靠拢
    for k in range(maxCycles):  # heavy on matrix operations
        h = sigmoid(dataMatrix * weights)  # matrix mult
        error = (labelMat - h)  # vector subtraction
        # dataMatrix.transpose()* error 就是梯度f(w)
        weights = weights + alpha * dataMatrix.transpose() * error  # matrix mult
    return weights


# 1. 画出各个训练点
# 2. 根据 weights(即回归的各个参数) 画出直线, 以便直观的看到划分是否正确
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    # 画点
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []
    ycord1 = []

    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')

    # 画线
    x1 = arange(-3.0, 3.0, 0.1)  # x1 取值区间为 [-3.0, 3.0), 步长为 0.1
    # 根据公式 0 = W0*X0 + W1*X1 + W2*X2 及 X0 = 1
    x2 = (-weights[0] - weights[1] * x1) / weights[2]
    ax.plot(x1, x2)
    plt.xlabel('X1')
    plt.ylabel('X2')

    # 显示
    plt.show()


if __name__ == "__main__":
    dataAttr, labelMat = loadDataSet()
    weights = gradAscent(dataAttr, labelMat)
    plotBestFit(weights.getA())
