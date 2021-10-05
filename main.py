import random
from graphics.graphics import *

def generateRandomPoints(N):
    points = []
    
    zoomOut = 0.9

    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    return list(set(points))

def init():

    # R: recursive
    # I: Iterative
    # S: superIterative
    # N: naive
    # t: collision test
    # m: manual
    # p: image
    # c: colission

    N = 30
    run(generateRandomPoints(N))


if __name__ == '__main__':
    init()
