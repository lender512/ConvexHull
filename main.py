import random
from graphics.graphics import *


def init():
    N = 100
    points = []

    zoomOut = 0.9

    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    testPoints = list(set(points))
    testPoints.sort(key=lambda x: x[0])

    runIterative(testPoints)
    #runRecursive(testPoints)




        

if __name__ == '__main__':
    init()
