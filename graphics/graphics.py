import sys, pygame
sys.path.append("..")
from functions.convexHull import *
from graphics.imageRecognition import *

pygame.init()
resize = 5

delay = 1000

size = width, height = int(360*resize), int(180*resize)
white = 255, 255, 255

screen = pygame.display.set_mode(size)

def normalizePoints(points):
    points.sort(key=lambda x: (x[1], x[0]))
    # print(points)
    currentY = 0
    first = False
    ranges = []
    counter = 0
    for i in range(len(points)):
        if points[i][1] != currentY:
            if counter >= 2:
                ranges.append(points[i-1])
            counter = 0
            first = False
        if not first:
            ranges.append(points[i])
            currentY = points[i][1]
            currentYIndex = i
            first = True
        counter += 1

    ranges.append(points[currentYIndex+counter-1])


    points = ranges
    points.sort(key=lambda x: (x[0], x[1]))


    currentX = 0
    first = False
    ranges = []
    counter = 0
    for i in range(len(points)):
        if points[i][0] != currentX:
            if counter >= 2:
                ranges.append(points[i-1])
            counter = 0
            first = False
        if not first:
            ranges.append(points[i])
            currentX = points[i][0]
            currentXIndex = i
            first = True
        counter += 1

    ranges.append(points[currentXIndex+counter-1])

    points = ranges
    points = list(set(points))
    points.sort(key=lambda x: x[0])

    return points



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

def convexHullIterative(pointList, delay):
    
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
        screen.fill(white)
        pygame.time.delay(delay)
        drawPoints(pointList)

    
    drawPoints(pointList)
    
    if len(nStack) == 1:
        pygame.draw.lines(screen, (10,10,10), True, transformList(nStack.pop()),1)

    else:
        pygame.draw.lines(screen, (10,10,10), True, transformList(stack.pop()),1)

    


def convexHullNaive(pointList, delay):
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
            pygame.time.delay(int(delay))
        p = q

        if(p == l):
            break

        pygame.display.flip()
        
    
    return hull

def runIterative(points, delay):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)

    convexHullIterative(points, delay)


    pygame.display.flip()
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
            pygame.draw.circle(screen, (255, 0, 0), transform(point), 10, 10)


        pygame.draw.lines(screen, (10,10,10), True, transformList(result),5)

        pygame.display.flip()

def runNaive(points, delay):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)

    result = convexHullNaive(points, delay)

    screen.fill(white)
    drawPoints(points)
    pygame.draw.lines(screen, (0,220,0), True, transformList(result),2)
    pygame.display.flip()

def transformImage(points):
    invertedList = []
    for point in points:
        invertedList.append((point[1], point[0])) 
    return invertedList

vel = 1

def down(points):
    for i in range(len(points)):
        points[i] = (points[i][0], points[i][1]+vel)

def up(points):
    for i in range(len(points)):
        points[i] = (points[i][0], points[i][1]-vel)

def left(points):
    for i in range(len(points)):
        points[i] = (points[i][0]-vel, points[i][1])

def right(points):
    for i in range(len(points)):
        points[i] = (points[i][0]+vel, points[i][1])

def runImage():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)
    

    points = edgeDetection()

    points = list(set(points))

    points = normalizePoints(points)

    # print(points)
    result = transformImage(convexHull(points))
    # print(result)

    screen.fill(white)
    pygame.draw.lines(screen, (220, 0, 0), True, transformImage(points), 1)

    path = os.getcwd() + '/graphics/test.jpg'

    screen.blit(pygame.image.load(path), [0, 0])
    pygame.display.flip()
    
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False

    pygame.draw.lines(screen, (0,0,0), True, result,3)
    pygame.display.flip()


    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            # handle MOUSEBUTTONUP

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    screen.fill(white)
                    down(result)
                    pygame.draw.lines(screen, (0,0,0), True, result,3)
                if event.key == pygame.K_UP:
                    screen.fill(white)
                    up(result)
                    pygame.draw.lines(screen, (0,0,0), True, result,3)
                if event.key == pygame.K_LEFT:
                    screen.fill(white)
                    left(result)
                    pygame.draw.lines(screen, (0,0,0), True, result,3)
                if event.key == pygame.K_RIGHT:
                    screen.fill(white)
                    right(result)
                    pygame.draw.lines(screen, (0,0,0), True, result,3)

        pygame.display.flip()

def runInteractive():
    points = []

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                points.append(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    nPoints = []
                    for point in points:
                        nPoints.append((point[0]-width//2, -(point[1]-height//2)))
                    runNaive(nPoints, 100)
                if event.key == pygame.K_i:
                    nPoints = []
                    for point in points:
                        nPoints.append((point[0]-width//2, -(point[1]-height//2)))
                    nPoints.sort(key=lambda x: x[0])
                    runIterative(nPoints, 1000)
                if event.key == pygame.K_r:
                    nPoints = []
                    for point in points:
                        nPoints.append((point[0]-width//2, -(point[1]-height//2)))
                    nPoints.sort(key=lambda x: x[0])
                    runRecursive(nPoints)

        screen.fill(white)

        for point in points:
            pygame.draw.circle(screen, (200, 0, 0), point, 4, 4)

        pygame.display.flip()


    return "uwu"

def isInPoly(polyA, polyB, delay):

    rightMostPointA = 0
    leftMostPointB = 0

    col = False

    for i in range(1, len(polyA)):
        if polyA[i][0]>polyA[rightMostPointA][0]:
            rightMostPointA = i

    a1 = rightMostPointA

    firsTime = False
    counter = 0
    for point in polyB:
        while clockwise(point, polyA[a1], polyA[(a1 + 1)%(len(polyA))])>=0 and not (a1 == rightMostPointA and firsTime):
            firsTime = True
            counter += 1
            a1 = (a1 + 1)%(len(polyA))
            pygame.draw.line(screen, (0,0,255), polyA[a1], point)
            # pygame.display.flip()
            pygame.time.delay(delay)
        if (counter == len(polyA)):
            print("ROJO ESTÁ DENTRO DE DE AZUL")
            col = True
        firsTime = False
        counter = 0


    for i in range(1, len(polyB)):
        if polyB[i][0]<polyB[leftMostPointB][0]:
            leftMostPointB = i

    b1 = leftMostPointB

    firsTime = False
    counter = 0
    for point in polyA:
        while clockwise(point, polyB[b1], polyB[(b1 + 1)%(len(polyB))])>=0 and not (b1 == leftMostPointB and firsTime):
            firsTime = True
            counter += 1
            b1 = (b1 + 1)%(len(polyB))
            pygame.draw.line(screen, (255,0,0), polyB[b1], point)
            # pygame.display.flip()
            pygame.time.delay(delay)
        if (counter == len(polyB)):
            print("AZUL ESTÁ DENTRO DE DE ROJO")
            col = True

        firsTime = False
        counter = 0

    return col


def runTest(polyA, polyB, delay):

    pos = (0,0)

    while 1:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(polyA)
                    resultA = convexHull(polyA)
                    print(resultA)
                    resultB = convexHull(polyB)
                    print(polyB)
                    print(resultB)
                    pygame.draw.lines(screen, (0, 0,255), True, transformList(resultA), 4)
                    pygame.draw.lines(screen, (255, 0, 0), True, transformList(resultB), 4)
                    pygame.display.flip()
                    isInPoly(transformList(resultA), transformList(resultB), delay)
                    wait = True
                    while wait:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                wait = False

    
        screen.fill(white)

        for point in transformList(polyA):
            pygame.draw.circle(screen, (0, 0, 255), point, 4, 4)

        for point in transformList(polyB):
            pygame.draw.circle(screen, (255, 0, 0), point, 4, 4)


        pygame.display.flip()


def runCollision():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)
    path1 = os.getcwd() + '/graphics/col1.jpg'
    points1 = edgeDetectionPath(path1)
    points1 = list(set(points1))
    points1 = normalizePoints(points1)
    result1 = convexHull(points1)


    path2 = os.getcwd() + '/graphics/col2.jpg'
    points2 = edgeDetectionPath(path2)
    points2 = list(set(points2))
    points2 = normalizePoints(points2)
    result2 = convexHull(points2)

    screen.fill(white)

    pos1 = (0,0)
    pos2 = (900, 0)


    screen.blit(pygame.image.load(path1).convert_alpha(), pos1)
    screen.blit(pygame.image.load(path2).convert_alpha(), pos2)

    for i in range(len(points1)):
        points1[i] = (points1[i][1] + pos1[0], points1[i][0] + pos1[1])
    for i in range(len(result1)):
        result1[i] = (result1[i][1] + pos1[0], result1[i][0] + pos1[1])

    # pygame.draw.lines(screen, (220, 0, 0), True, points1, 1)

    for i in range(len(points2)):
        points2[i] = (points2[i][1] + pos2[0], points2[i][0] + pos2[1])
    for i in range(len(result2)):
        result2[i] = (result2[i][1] + pos2[0], result2[i][0] + pos2[1])

    # pygame.draw.lines(screen, (220, 0, 0), True, points2, 1)
    
    pygame.display.flip()
    
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False

    pygame.draw.lines(screen, (0,0,0), True, result1,3)
    pygame.draw.lines(screen, (0,0,0), True, result2,3)
    pygame.display.flip()

    img1 = pygame.image.load(path1).convert()
    img1.set_alpha(70)
    # tImg1.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
    img2 = pygame.image.load(path2).convert()
    img2.set_alpha(70)

    # tImg2 = img2.copy()
    # tImg2.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            screen.fill(white)
            down(result2)
            pos2 = (pos2[0], pos2[1]+vel)

        if keys[pygame.K_UP]:
            screen.fill(white)
            up(result2)
            pos2 = (pos2[0], pos2[1]-vel)

        if keys[pygame.K_LEFT]:
            screen.fill(white)
            left(result2)
            pos2 = (pos2[0]-vel, pos2[1])

        if keys[pygame.K_RIGHT]:
            screen.fill(white)
            right(result2)
            pos2 = (pos2[0]+vel, pos2[1])

        if isInPoly(result1, result2, 0):
            pygame.draw.circle(screen, (0, 0, 255), (width//2, height//2), 40, 4)
        screen.blit(img1, pos1)
        pygame.draw.lines(screen, (0,0,255), True, result1,3)   
        screen.blit(img2, pos2)
        pygame.draw.lines(screen, (255,0,0), True, result2,3)

        pygame.display.flip()