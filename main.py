import sys, pygame, random
from functions.convexHull import *


pygame.init()
resize = 5

size = width, height = 360*resize, 180*resize
speed = [2, 2]
white = 255, 255, 255
col_lineG = 255, 0, 0
col_lineA = 0, 0, 255

screen = pygame.display.set_mode(size)

points = [(0, 0), (0, 4), (-4, 0), (5, 0), (0, -6), (1, 0)]
#(-4, 0), (5, 0), (0, -6), (0, 4)

def transform(point):
    return ((width//2 + point[0], -point[1]+height//2))

def transformList(list):
    list2 = []
    for i in range(len(list)):
        list2.append(transform(list[i]))
    return list2


def init():

    # print(convexHullBase([(-125, 123), (-100,14), (-54, 45)]))
    # print(convexHullBase1([(-125, 123), (-100,14), (-54, 45)]))

    N = 1000
    points = []

    pointsHuby = [(-810,130),(-810,92),(-809,-380),(-805,-385),(-554,-405),(608,-401),(749,-398),(774,-392),(810,-226),(809,202),(801,325),(783,352),(758,367),(668,394),(404,403),(-58,405),(-650,403),(-797,393),(-802,310)]
    pointsLender = [(-58, 405), (-650, 403), (-797, 393), (-802, 310), (-810, 130), (-810, 92), (-809, -380), (-805, -385), (-554, -405), (24, -403), (480, -398), (520, -382), (540, -280), (540, -233), (540, -262), (546, -355), (560, -401), (608, -401), (749, -398), (774, -392), (810, -226), (809, 202), (801, 325), (783, 352), (758, 367), (668, 394), (404, 403)]

    zoomOut = 0.9
    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    #points = [(-126, 296), (-638,4), (-786,-447), (202,-84), (230, -355), (350, -362)]
    testPoints = list(set(points))

    testPoints.sort(key=lambda x: x[0])
    
    string = ""
    for point in testPoints:
        string += "{" + str(point[0]) + "," + str(point[1]) + "}, "

    print("{",string,"}")

    result = convexHull(testPoints)

    print(result)

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        screen.fill(white)

        
        

        for point in testPoints:
            pygame.draw.circle(screen, (100, 100, 100), transform(point), 5, 5)

        for point in result:
            pygame.draw.circle(screen, (255, 0, 0), transform(point), 10, 2)


        # for point in pointsHuby:
        #     pygame.draw.circle(screen, (0, 0, 255), transform(point), 10, 2)

        # for point in pointsLender:
        #     pygame.draw.circle(screen, (0, 255, 0), transform(point), 10, 2)

        pygame.draw.lines(screen, (10,10,10), True, transformList(result),5)
        # pygame.draw.lines(screen, (0,0,255), True, transformList(pointsHuby),5)
        # pygame.draw.lines(screen, (0,255,0), True, transformList(pointsLender),5)

        pygame.display.flip()

if __name__ == '__main__':
    init()
