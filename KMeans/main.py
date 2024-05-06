import math
import sys
from random import shuffle, uniform


def ReadData(filename):
    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()

    items = []

    for i in range(len(lines)):
        line = lines[i].split(' . ')
        itemFeatures = []

        for j in range(len(line)):
            v = float(line[j])
            itemFeatures.append(v)

        items.append(itemFeatures)
    shuffle(items)
    return items


def find_col_min_max(items):
    n = len(items[0])
    mini = [sys.maxint for i in range(n)]
    maxi = [-sys.maxint -1 for i in range(n)]

    for item in items:
        for f in range(len(item)):
            if item[f] < mini[f]:
                mini[f] = item[f]
            if item[f] > maxi[f]:
                maxi[f] = item[f]
    return mini, maxi


def InitializeMeans(items, k, cMin, cMax):
    f = len(items[0])
    means = [[0 for i in range(f)] for j in range(k)]

    for mean in means:
        for i in range(len(means)):
            mean[i] = uniform(cMin[i] + 1, cMax[i] - 1)
    return means


def EuclideanDistance(x, y):
    dist = 0
    for i in range(len(x)):
        dist += math.pow(x[i] - y[i], 2)
    return math.sqrt(dist)


def UpdateMeans(n, mean, items):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1) + items[i]) / float(n)
        mean[i] = round(m, 3)
    return mean


def Classify(means, item):
    minimum = sys.maxint
    index = -1

    for i in range(len(means)):
        dist = EuclideanDistance(means[i], item)
        if dist < minimum:
            minimum = dist
            index = i

    return index


def CalculateMeans(k, items, maxIterations = 100000):
    cMin, cMax = find_col_min_max(items)
    means = InitializeMeans(items, k, cMin, cMax)
    clusterSizes = [0 for i in range(len(means))]
    belongsTo = [0 for i in range(len(items))]


    for i in range(maxIterations):
        noChange = True
        for i in range (len(items)):
            item = items[i]
            index = Classify(means, item)

            clusterSizes[index] += 1
            cSize = clusterSizes[index]
            means[index] = UpdateMeans(cSize, means[index], [item])

            if index != belongsTo[i]:
                noChange = False
            belongsTo[i] = index
            if (noChange):
                break

    return means


def findClusters(means, items):
    clusters = [[] for i in range(len(means))]

    for item in items:
        index = Classify(means, items)
        clusters[index].append(item)

    return clusters






