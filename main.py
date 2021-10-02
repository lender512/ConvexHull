import random
from graphics.graphics import *


def init():
    # while 1:
    N = 1000000
    points = []

    zoomOut = 0.9

    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    testPoints = list(set(points))

    testPoints.sort(key=lambda x: x[1])
    
    currentY = 0
    first = False
    ranges = []
    for i in range(len(testPoints)):
        if not first:
            ranges.append(testPoints[i])
            currentY = testPoints[i][1]
            first = True
        lastPoint = i
        if testPoints[i][0] != currentY:
            ranges.append(testPoints[i-1])
            first = False

    testPoints = ranges

    testPoints.sort(key=lambda x: x[0])


    currentX = 0
    first = False
    ranges = []
    for i in range(len(testPoints)):
        if not first:
            ranges.append(testPoints[i])
            currentX = testPoints[i][0]
            first = True
        lastPoint = i
        if testPoints[i][0] != currentX:
            ranges.append(testPoints[i-1])
            first = False

    testPoints = ranges


    testPoints = list(set(testPoints))
    edgeDetection()
    testPoints.sort(key=lambda x: x[0])


    runIterative(testPoints)
    # runNaive(testPoints)
    # runRecursive(testPoints)
    # runImage()
    
        

if __name__ == '__main__':
    init()
