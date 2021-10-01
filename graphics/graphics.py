import sys, pygame
sys.path.append("..")
from functions.convexHull import *

pygame.init()
resize = 5

delay = 1000

size = width, height = int(360*resize), int(180*resize)
white = 255, 255, 255

screen = pygame.display.set_mode(size)

def transform(point):
    return ((width//2 + point[0], -point[1]+height//2))

def transformList(list):
    list2 = []
    for i in range(len(list)):
        list2.append(transform(list[i]))
    return list2


def drawPoints(pointList):
    for point in pointList:
        pygame.draw.circle(screen, (100, 100, 100), transform(point), 2, 1)

def convexHullIterative(pointList):
    
    drawPoints(pointList)

    stack = []
    stack.append(pointList)

    nStack = []

    pygame.display.flip()
    pygame.time.delay(delay)

    while not len(stack) == 0:
        top = stack.pop()


        if len(top) <= 5:
            nStack.append(convexHullBase(top))
        
        else:
            left = top[0:len(top)//2]
            right = top[len(top)//2:]

            stack.append(right)
            stack.append(left)
    
    for polygon in nStack:
        pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),1)
    pygame.display.flip()
    pygame.time.delay(delay)
    
    screen.fill(white)
    drawPoints(pointList)

    while not (len(nStack) == 1 or len(stack) == 1):
        while len(nStack) >= 2:
            top2 = nStack.pop()
            top1 = nStack.pop()
            stack.append(convexHullMerge(top1,top2))

            for polygon in stack:
                pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),1)
        
        pygame.display.flip()
        pygame.time.delay(delay)
        screen.fill(white)
        drawPoints(pointList)

        while len(stack) >= 2:
            top1 = stack.pop()
            top2 = stack.pop()
            nStack.append(convexHullMerge(top1,top2))

            for polygon in nStack:
                pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),1)

        pygame.display.flip()
        pygame.time.delay(delay)
        screen.fill(white)
        drawPoints(pointList)

    
    drawPoints(pointList)
    

    for polygon in nStack:
        pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),1)

    for polygon in stack:
        pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),1)

def runIterative(points):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)

    result = convexHullIterative(points)

    while 1:
        pygame.time.delay(delay)

def runRecursive(points):
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        screen.fill(white)

        result = convexHull(points)

        for point in points:
            pygame.draw.circle(screen, (100, 100, 100), transform(point), 5, 5)

        for point in result:
            pygame.draw.circle(screen, (255, 0, 0), transform(point), 10, 2)


        pygame.draw.lines(screen, (10,10,10), True, transformList(result),5)
        # pygame.draw.lines(screen, (0,0,255), True, transformList(pointsHuby),5)
        # pygame.draw.lines(screen, (0,255,0), True, transformList(pointsLender),5)

        pygame.display.flip()