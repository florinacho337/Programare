import math
from random import *
import random
from math import dist
import matplotlib.pyplot
from matplotlib import pyplot as plt


def randomPoint():
    tup = (random.random(),random.random())
    return tup


def cerc(n: int):
    cerc = 0
    plt.axis([0, 1, 0, 1])
    for i in range(n):
        x, y = randomPoint()
        distance = math.dist([0.5, 0.5], [x, y])
        if distance < 0.5:
            cerc += 1
    print("i)")
    sim = cerc/n
    res = math.pi / 4
    print(sim)
    print(res)
    print("eroare ", abs(sim - res), "\n")

    return cerc / n

def cercPlot(n):
    xs = []
    ys = []
    cxs = []
    cys = []
    plt.axis([0, 1, 0, 1])
    for i in range(n):
        x, y = randomPoint()
        distance = math.dist([0.5, 0.5], [x, y])
        if distance < 0.5:
            cxs.append(x)
            cys.append(y)
        else:
            xs.append(x)
            ys.append(y)

    plt.plot(xs, ys, 'bo')
    plt.plot(cxs, cys, 'ro')
    plt.show()

def centru(n: int):
    corect = 0
    xs = []
    ys = []
    cxs = []
    cys = []
    plt.axis([0, 1, 0, 1])
    for i in range(n):
        x, y = random.random(), random.random()
        dists = [math.dist([1.0, 1.0], [x, y]), math.dist([0.0, 1.0], [x, y]),
                 math.dist([1.0, 0.0], [x, y]), math.dist([0.0, 0.0], [x, y])]
        distCentru = math.dist([0.5, 0.5], [x, y])
        ok = True
        for j in range(4):
            if distCentru > dists[j]:
                ok = False
                break
        if ok:
            cxs.append(x)
            cys.append(y)
            corect += 1
        else:
            xs.append(x)
            ys.append(y)

    print("ii)")
    sim = corect/n
    res = 1 / 2
    print(sim)
    print(res)
    print("Err: ", abs(sim - res), "\n")

def centruPlot(n):
    xs = []
    ys = []
    cxs = []
    cys = []
    plt.axis([0, 1, 0, 1])
    for i in range(n):
        x, y = randomPoint()
        dists = [math.dist([1.0, 1.0], [x, y]), math.dist([0.0, 1.0], [x, y]),
                 math.dist([1.0, 0.0], [x, y]), math.dist([0.0, 0.0], [x, y])]
        distsc = math.dist([0.5, 0.5], [x, y])
        continua = True
        for j in range(4):
            if distsc > dists[j]:
                ok = False
                break
        if continua:
            cxs.append(x)
            cys.append(y)
        else:
            xs.append(x)
            ys.append(y)

    plt.plot(xs, ys, 'bo'), plt.plot(cxs, cys, 'ro'), plt.show()


def triunghiuri(n: int):
    triunghiuri = 0
    raza = 0.5
    plt.axis([0, 1, 0, 1])

    for i in range(0,n):
        x, y = randomPoint()
        dists = [math.dist([0.5, 0.0], [x, y]), math.dist([0.0, 0.5], [x, y]),
                 math.dist([0.5, 1.0], [x, y]), math.dist([1.0, 0.5], [x, y])]
        puncte = 0
        for d in dists:
            if d<raza:
                puncte += 1
        if puncte >= 2:
            triunghiuri += 1
    print("iii)")
    sim = triunghiuri/n
    res = math.pi / 2 - 1
    print(sim)
    print(res)
    print("eroare", abs(sim - res), "\n")
    return triunghiuri / n

def plotTriunghi(n):
    raza = 0.5
    xs = []
    ys = []
    cxs = []
    cys = []
    plt.axis([0, 1, 0, 1])

    for i in range(0, n):
        x, y = randomPoint()
        dists = [math.dist([0.5, 0.0], [x, y]), math.dist([0.0, 0.5], [x, y]),
                 math.dist([0.5, 1.0], [x, y]), math.dist([1.0, 0.5], [x, y])]
        puncte = 0
        for d in dists:
            if d < raza:
                puncte += 1
        if puncte >= 2:
            cxs.append(x)
            cys.append(y)
        else:
            xs.append(x)
            ys.append(y)

    plt.plot(xs, ys, 'bo')
    plt.plot(cxs, cys, 'ro')
    plt.show()


if __name__ == '__main__':
    cerc(1000)
    cercPlot(1000)
    centru(1000)
    centruPlot(1000)
    triunghiuri(1000)
    plotTriunghi(1000)