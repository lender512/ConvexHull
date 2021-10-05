import sys, pygame, math
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

def convexHullMergeIterative(PointListA, PointListB):
    
    rightMostPointA = 0
    leftMostPointB = 0
    
    for i in range(1, len(PointListA)):
        if PointListA[i][0]>PointListA[rightMostPointA][0]:
            rightMostPointA = i
        # elif PointListA[i][0]==PointListA[rightMostPointA][0]:
        #     if PointListA[i][1]<PointListA[rightMostPointA][1]:
        #         rightMostPointA = i


    for i in range(1, len(PointListB)):
        if PointListB[i][0]<PointListB[leftMostPointB][0]:
            leftMostPointB = i
        # elif PointListB[i][0]==PointListB[leftMostPointB][0]:
        #     if PointListB[i][1]<PointListB[leftMostPointB][1]:
        #         leftMostPointB = i


    done = False
    a1 = rightMostPointA
    b1 = leftMostPointB
    
    while not done:
        
        # screen.fill(white)
        pygame.draw.lines(screen, (0,255,0), True, transformList(PointListA),2)
        pygame.draw.lines(screen, (0,255,0), True, transformList(PointListB),2)
        pygame.display.flip()

        pygame.draw.line(screen, (0,0,255), transform(PointListB[b1]), transform(PointListA[a1]), 1)
        pygame.display.flip()
        pygame.time.delay(1000)

        done = True
        while clockwise(PointListB[b1], PointListA[a1], PointListA[(a1 + 1)%(len(PointListA))])>=0:
            a1 = (a1 + 1)%(len(PointListA))
            pygame.draw.line(screen, (0,0,255), transform(PointListB[b1]), transform(PointListA[a1]), 1)
            pygame.display.flip()
            pygame.time.delay(1000)
            
        while clockwise(PointListA[a1], PointListB[b1], PointListB[(len(PointListB)+b1-1)%(len(PointListB))])<=0:
            b1 = (len(PointListB)+b1-1)%(len(PointListB))
            done = False
            pygame.draw.line(screen, (0,0,255), transform(PointListA[a1]), transform(PointListB[b1]), 1)
            pygame.display.flip()
            pygame.time.delay(1000)

    upperA = a1
    upperB = b1

    pygame.draw.line(screen, (255,0,0), transform(PointListB[upperB]), transform(PointListA[upperA]), 2)
    pygame.display.flip()
    pygame.time.delay(1000)


    done = False
    a1 = rightMostPointA
    b1 = leftMostPointB
    while not done:

        #screen.fill(white)
        pygame.draw.line(screen, (255,0,0), transform(PointListB[upperB]), transform(PointListA[upperA]), 2)
        pygame.draw.lines(screen, (0,255,0), True, transformList(PointListA),2)
        pygame.draw.lines(screen, (0,255,0), True, transformList(PointListB),2)
        pygame.display.flip()

        done = True
        while clockwise(PointListA[a1], PointListB[b1], PointListB[(b1 + 1)%(len(PointListB))])>=0:
            b1 = (b1 + 1)%(len(PointListB))
            
            pygame.draw.line(screen, (0,0,255), transform(PointListA[a1]), transform(PointListB[b1]), 1)
            pygame.display.flip()
            pygame.time.delay(1000)
            # print(PointListA[a1], PointListB[b1], PointListB[(b1 + 1)%(len(PointListB))])
    
            
        while clockwise(PointListB[b1], PointListA[a1], PointListA[(len(PointListA)+a1-1)%(len(PointListA))])<=0:
            a1 = (len(PointListA)+a1-1)%(len(PointListA))
            done = False
            pygame.draw.line(screen, (0,0,255), transform(PointListB[b1]), transform(PointListA[a1]), 1)
            pygame.display.flip()
            pygame.time.delay(1000)


    lowerA = a1
    lowerB = b1

    pygame.draw.line(screen, (255,0,0), transform(PointListB[lowerB]), transform(PointListA[lowerA]), 2)
    pygame.display.flip()
    pygame.time.delay(1000)

    mergeList = []
    mergeList.append(PointListA[upperA])

    while upperA != lowerA:
        upperA = (upperA+1)%len(PointListA)
        mergeList.append(PointListA[upperA])
    
    mergeList.append(PointListB[lowerB])
    while lowerB != upperB:
        lowerB = (lowerB+1)%len(PointListB)
        mergeList.append(PointListB[lowerB])
    
    return mergeList

def convexHullIterative(pointList, delay ,superIterative):
    
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
        pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),2)
    pygame.display.flip()
    pygame.time.delay(delay)
    
    #screen.fill(white)
    drawPoints(pointList)

    while not (len(nStack) == 1 or len(stack) == 1):
        while len(nStack) >= 2:
            top2 = nStack.pop()
            top1 = nStack.pop()
            if superIterative:
                stack.append(convexHullMergeIterative(top1,top2))
            else:
                stack.append(convexHullMerge(top1,top2))

            for polygon in stack:
                pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),2)
        
        pygame.display.flip()
        pygame.time.delay(delay)
        screen.fill(white)
        drawPoints(pointList)

        while len(stack) >= 2:
            top1 = stack.pop()
            top2 = stack.pop()
            if superIterative:
                nStack.append(convexHullMergeIterative(top1,top2))
            else:
                nStack.append(convexHullMerge(top1,top2))

            for polygon in nStack:
                pygame.draw.lines(screen, (10,10,10), True, transformList(polygon),2)

        pygame.display.flip()
        screen.fill(white)
        pygame.time.delay(delay)
        drawPoints(pointList)

    
    drawPoints(pointList)
    
    if len(nStack) == 1:
        pygame.draw.lines(screen, (10,10,10), True, transformList(nStack.pop()),2)

    else:
        pygame.draw.lines(screen, (10,10,10), True, transformList(stack.pop()),2)

    


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

def runIterative(points, delay, superIterative):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)

    convexHullIterative(points, delay, superIterative)


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
    pygame.draw.lines(screen, (220, 0, 0), True, transformImage(points), 2)

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
                    runIterative(nPoints, 1000, False)
                if event.key == pygame.K_s:
                    nPoints = []
                    for point in points:
                        nPoints.append((point[0]-width//2, -(point[1]-height//2)))
                    nPoints.sort(key=lambda x: x[0])
                    runIterative(nPoints, 1000, True)
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
            pygame.draw.line(screen, (0,0,255), polyA[a1], point, 1)
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
            pygame.draw.line(screen, (255,0,0), polyB[b1], point, 1)
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

                    resultA = convexHull(polyA)
                    resultB = convexHull(polyB)
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

def transformRotate(origin, point, angle):
    ox = origin[0]
    oy = origin[1]
    px = point[0]
    py = point[1]

    angle = math.radians(angle)
    x1 = ox - px;
    y1 = oy - py;

    temp = (x1 * math.cos(angle)) - (y1 * math.sin(angle));
    y1   = (x1 * math.sin(angle)) + (y1 * math.cos(angle));
    x1   = temp;
    return (x1 + px, y1 + py)



def runCollision():

    stop = pygame.image.load(os.getcwd() + "/graphics/stop.png")

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
    center1 = img1.get_rect().center
    # tImg1.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
    img2 = pygame.image.load(path2).convert()
    img2.set_alpha(70)
    center2 = (img2.get_rect().center[0] + pos2[0], img2.get_rect().center[1] + pos2[1])


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
            center2 = (center2[0], center2[1]+vel)


        if keys[pygame.K_UP]:
            screen.fill(white)
            up(result2)
            pos2 = (pos2[0], pos2[1]-vel)
            center2 = (center2[0], center2[1]-vel)

        if keys[pygame.K_LEFT]:
            screen.fill(white)
            left(result2)
            pos2 = (pos2[0]-vel, pos2[1])
            center2 = (center2[0]-vel, center2[1])

        if keys[pygame.K_RIGHT]:
            screen.fill(white)
            right(result2)
            pos2 = (pos2[0]+vel, pos2[1])
            center2 = (center2[0]+vel, center2[1])


        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            screen.fill(white)
            down(result1)
            pos1 = (pos1[0], pos1[1]+vel)
            center1 = (center1[0], center1[1]+vel)

        if keys[pygame.K_w]:
            screen.fill(white)
            up(result1)
            pos1 = (pos1[0], pos1[1]-vel)
            center1 = (center1[0], center1[1]-vel)

        if keys[pygame.K_a]:
            screen.fill(white)
            left(result1)
            pos1 = (pos1[0]-vel, pos1[1])
            center1 = (center1[0]-vel, center1[1])

        if keys[pygame.K_d]:
            screen.fill(white)
            right(result1)
            pos1 = (pos1[0]+vel, pos1[1])
            center1 = (center1[0]+vel, center1[1])

        if isInPoly(result1, result2, 0):
            rect = stop.get_rect()
            rect.center = (width//2, height//2)
            screen.blit(stop, rect)


        screen.blit(img1, pos1)
        pygame.draw.lines(screen, (0,0,255), True, result1,3)   
        screen.blit(img2, pos2)
        pygame.draw.lines(screen, (255,0,0), True, result2,3)

        pygame.draw.circle(screen,(0, 0, 255), center1 , 5)
        pygame.draw.circle(screen,(255, 0, 0), center2 , 5)

        pygame.display.flip()

def run(points):
    # runImage()

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    runRecursive(normalizePoints(points))
                if event.key == pygame.K_i:
                    runIterative(normalizePoints(points), 1000, False)
                if event.key == pygame.K_s:
                    runIterative(normalizePoints(points), 100, True)
                if event.key == pygame.K_n:
                    runNaive(normalizePoints(points), 1000)
                if event.key == pygame.K_t:
                    testPoints1 = points[0:len(points)//2]
                    testPoints2 = points[len(points)//2:]
                    testPoints1 = normalizePoints(testPoints1)
                    testPoints2 = normalizePoints(testPoints2)
                    runTest(testPoints1, testPoints2, 100)
                if event.key == pygame.K_m:
                    runInteractive() 
                if event.key == pygame.K_p:
                    runImage()
                if event.key == pygame.K_c:
                    runCollision()
        screen.fill(white)

    runCollision()