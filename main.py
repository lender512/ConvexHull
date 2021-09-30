import sys, pygame, random
from functions.convexHull import convexHull


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
    N = 100
    points = []
    zoomOut = 0.9
    for n in range(N):
        points.append((random.randint(-width//2*zoomOut, width//2*zoomOut),(random.randint(-height//2*zoomOut, height//2*zoomOut)))) 

    #points = [(-126, 296), (-638,4), (-786,-447), (202,-84), (230, -355), (350, -362)]
    testPoints = points
    testPoints.sort(key=lambda x: x[0])
    
    result = convexHull(testPoints)

    print(result)

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        screen.fill(white)

        

        for point in testPoints:
            pygame.draw.circle(screen, (100, 100, 100), transform(point), 5, 5)

        for point in result:
            pygame.draw.circle(screen, (0, 0, 0), transform(point), 5, 2)

        pygame.draw.lines(screen, (10,10,10), True, transformList(result),5)

        pygame.display.flip()

if __name__ == '__main__':
    init()
