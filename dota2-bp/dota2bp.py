import json
import pandas as pd
import numpy as np
import pickle
import time

# init effect matrix
# if hero A and B in the same side and they win / lose, then the effect of A to B and B to A + 1 / - 1
effectMatrix_X = np.zeros((113, 113), dtype=np.float64)
# if hero A and B in the different side and A win, then the effect of A to B - 1, the effect of B to A + 1
effectMatrix_Y = np.zeros((113, 113), dtype=np.float64)
# init count matrix
countMatrix_X = np.zeros((113, 113), dtype=np.int64)
countMatrix_Y = np.zeros((113, 113), dtype=np.int64)


def getHeroList(url):
    with open(url, encoding='UTF-8') as f:
        heroList = json.load(f)["heroes"]
    return heroList


def getEffectMatrix(data):
    length = len(data)
    for i in range(length):
        # for i in range(1):
        match = data.iloc[i].values

        # get match result messages
        team = match[0]
        clusterId = match[1]
        gameMode = match[2]
        gameType = match[3]
        heroes = match[4:]

        # add the win heroes & lose heroes to the sets
        winArray = []
        loseArray = []
        for j in range(len(heroes)):
            if heroes[j] == 0:
                continue
            elif heroes[j] == team:
                winArray.append(j)
            elif heroes[j] == -team:
                loseArray.append(j)

        # add the effect into the matrixs

        # the same side effect
        for i in range(5):
            for j in range(5):
                x, y = winArray[i], winArray[j]
                effectMatrix_X[x][y] += 1
                countMatrix_X[x][y] += 1
        for i in range(5):
            for j in range(5):
                x, y = loseArray[i], loseArray[j]
                effectMatrix_X[x][y] -= 1
                countMatrix_X[x][y] += 1
        # the different side effect
        for i in range(5):
            for j in range(5):
                x, y = winArray[i], loseArray[j]
                effectMatrix_Y[x][y] -= 1  # effect hero x to hero y
                effectMatrix_Y[y][x] += 1  # effect hero y to hero x
                countMatrix_Y[x][y] += 1
                countMatrix_Y[y][x] += 1

    res_X = np.zeros((113,113), dtype=np.float64)
    res_Y = np.zeros((113,113), dtype=np.float64)
    for i in range(113):
        for j in range(113):
         res_X[i][j] = effectMatrix_X[i][j] / countMatrix_X[i][j] if countMatrix_X[i][j] != 0 else 0
         res_Y[i][j] = effectMatrix_Y[i][j] / countMatrix_Y[i][j] if countMatrix_Y[i][j] != 0 else 0
    return res_X, res_Y


def dump(matrix, url):
    with open(url, 'wb') as f:
        pickle.dump(matrix, f)


def load(url):
    with open(url, 'rb') as f:
        return pickle.load(f)


# pickList is a set composed of the ids of the heroes having been picked
# banList is a set composed of the ids of the heroes having been banned
def getPickAdvise(em_X, em_Y, pickList_A, pickList_B, banList):
    return getBestPick(em_X, em_Y, pickList_A, pickList_B, banList)


def getBanAdvise(em_X, em_Y, pickList_A, pickList_B, banList):
    return getBestPick(em_X, em_Y, pickList_B, pickList_A, banList)


def getBestPick(em_X, em_Y, pickList_A, pickList_B, banList):
    arr = np.array([0]*113, dtype=np.float64)
    if pickList_A == [] and pickList_B == []:
        for line in em_X:
            arr += line
        for line in em_Y:
            arr += line
    else:
        for hero in pickList_A:
            arr += np.array(em_Y[hero])
        for hero in pickList_B:
            arr += np.array(em_X[hero])

    # find the best pick choice
    bestPick = np.argmax(arr)
    while bestPick in banList or bestPick in pickList_A or bestPick in pickList_B:
        arr[bestPick] = -2147483648
        bestPick = np.argmax(arr)
    return bestPick


if __name__ == "__main__":
    startTime = time.time()
    train = pd.read_csv('data\dota2Train.csv', header=None)
    test = pd.read_csv('data\dota2Test.csv', header=None)
    data = pd.concat([train, test], ignore_index=True)
    A, B = getEffectMatrix(data)
    dump(A, 'matrix_A.pkl')
    dump(B, 'matrix_B.pkl')
    endTime = time.time()
    print("共耗时", round(endTime - startTime, 2), "secs")