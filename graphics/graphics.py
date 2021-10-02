import sys, pygame
sys.path.append("..")
from functions.convexHull import *
from graphics.imageRecognition import *

pygame.init()
resize = 5

delay = 100

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
        pygame.draw.circle(screen, (100, 100, 100), transform(point), 2,2)

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


def convexHullNaive(pointList):
    if len(pointList) < 3:
        return pointList
 
    l = Left_index(pointList)
    
    hull = []
     
    p = l
    q = 0
    while(True):
         
        hull.append(pointList[p])
        drawPoints(pointList)
        for point in hull:
            pygame.draw.circle(screen, (220, 0, 0), transform(point), 4, 4)

        q = (p + 1) % len(pointList)
        if len(hull) > 1:
            pygame.draw.lines(screen, (220,0,0), False, transformList(hull),2)
        for i in range(len(pointList)):
            if len(hull) > 1:
                pygame.draw.lines(screen, (220,0,0), False, transformList(hull),2)
            if(clockwise(pointList[p],pointList[q], pointList[i]) == 1):
                q = i
            pygame.draw.line(screen, (220, 0, 0), transform(pointList[p]), transform(pointList[i]), 3)
            pygame.draw.line(screen, (0, 220, 0), transform(pointList[p]), transform(pointList[q]), 3)
            pygame.display.flip()
            screen.fill(white)
            drawPoints(pointList)
            for point in hull:
                pygame.draw.circle(screen, (220, 0, 0), transform(point), 4, 4)
            pygame.time.delay(int(delay/10))
        p = q

        if(p == l):
            break

        pygame.display.flip()
        
    
    return hull

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

def runNaive(points):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)

    result = convexHullNaive(points)

    screen.fill(white)
    drawPoints(points)
    pygame.draw.lines(screen, (0,220,0), True, transformList(result),2)
    pygame.display.flip()

def transformImage(points):
    invertedList = []
    for point in points:
        invertedList.append((point[1], point[0])) 
    return invertedList

def runImage():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)
    

    points = edgeDetection()

    points = list(set(points))

    points.sort(key=lambda x: x[1])
    
    currentY = 0
    first = False
    ranges = []
    for i in range(len(points)):
        if not first:
            ranges.append(points[i])
            currentY = points[i][1]
            first = True
        lastPoint = i
        if points[i][1] != currentY:
            ranges.append(points[i-1])
            first = False

    points = ranges

    points.sort(key=lambda x: x[0])


    currentX = 0
    first = False
    ranges = []
    for i in range(len(points)):
        if not first:
            ranges.append(points[i])
            currentX = points[i][0]
            first = True
        lastPoint = i
        if points[i][0] != currentX:
            ranges.append(points[i-1])
            first = False

    points = ranges


    points = list(set(points))
    points.sort(key=lambda x: x[0])

    print(points)
    result = transformImage(convexHull(points))
    print(result)

    screen.fill(white)
    pygame.draw.lines(screen, (220, 0, 0), True, transformImage(points), 1)

    screen.blit(pygame.image.load("test.jpg"), [0, 0])
    pygame.draw.lines(screen, (0,0,0), True, result,5)
    pygame.display.flip()


    while 1:
        pygame.time.delay(delay)