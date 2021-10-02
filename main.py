import random
from graphics.graphics import *

def generateRandomPoints(N):
    points = []
    
    zoomOut = 0.9

    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    return list(set(points))

def init():
    # while 1:
    N = 10

    # test = [(100, 10), (100, 70), (54, 123) , (23, 123), (100, 123)]
    # print(normalizePoints(test))

    testPoints = generateRandomPoints(N)
    
    testPoints = normalizePoints(testPoints)

    # runIterative(testPoints, 100)
    # runNaive(testPoints)
    # runRecursive(testPoints)
    # runImage()
    
    #press (R)ecursive, (I)terative or (N)aive
    runInteractive() 




if __name__ == '__main__':
    init()
