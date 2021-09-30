from functools import cmp_to_key


mid = (0, 0)


def clockwise(a, b, c):
    result = (b[1]-a[1])*(c[0]-b[0]) - (c[1]-b[1])*(b[0]-a[0])

    if result == 0:
        return 0
    if result > 0:
        return 1
    return -1


def quad(point):
    if point[0] >= 0 and point[1] >= 0:
        return 1
    if point[0] <= 0 and point[1] >= 0:
        return 2
    if point[0] <= 0 and point[1] <= 0:
        return 3
    return 4

def compare(pointA, pointB):
    global mid
    p = (pointA[0] - mid[0], pointA[1] - mid[1])
    q = (pointB[0] - mid[0], pointB[1] - mid[1])

    one = quad(p)
    two = quad(q)

    if one != two:
        return (one < two)
    return ((p[1]*q[0] < q[1]*p[0]))

def bubbleSort(arr):
    n = len(arr)
 
    for i in range(n-1):
 
        for j in range(0, n-i-1):
 
            if not compare(arr[j], arr[j + 1]) :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def convexHullBase(points):
    lista = []
    
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            x1 = points[i][0]
            y1 = points[i][1]
            x2 = points[j][0]
            y2 = points[j][1]

            a1 = y1-y2
            b1 = x2-x1
            c1 = x1*y2-y1*x2
            
            pos = 0
            neg = 0

            for k in range(len(points)):
                if a1*points[k][0] + b1*points[k][1] + c1 <= 0:
                    neg = neg + 1
                if a1*points[k][0] + b1*points[k][1] + c1 >= 0:
                    pos = pos + 1
            
            if pos == len(points) or neg == len(points):
                lista.append(points[i])
                lista.append(points[j])

    lista = set(lista)

    lista = list(lista)
    
    global mid
    mid = (0,0)
    n = len(lista)
    for i in range(n):
        mid = (mid[0] + lista[i][0], mid[1] +lista[i][1])
        lista[i]=(lista[i][0]*n, lista[i][1]*n)
    
    
    bubbleSort(lista)

    for i in range(n):
        lista[i] = (lista[i][0]//n, lista[i][1]//n)

    return lista
        
def convexHullMerge(PointListA, PointListB):
    
    rightMostPointA = 0
    leftMostPointB = 0
    
    for i in range(1, len(PointListA)):
        if PointListA[i][0]>PointListA[rightMostPointA][0]:
            rightMostPointA = i


    for i in range(1, len(PointListB)):
        if PointListB[i][0]<PointListB[leftMostPointB][0]:
            leftMostPointB = i


    done = False
    a1 = rightMostPointA
    b1 = leftMostPointB
    
    while not done:
        a2 = (a1 + 1)%(len(PointListA))
        b2 = (len(PointListB)+b1-1)%(len(PointListB))
        
        done = True
        while clockwise(PointListB[b1], PointListA[a1], PointListA[(a1 + 1)%(len(PointListA))])>=0:
            a1 = (a1 + 1)%(len(PointListA))
            
        while clockwise(PointListA[a1], PointListB[b1], PointListB[(len(PointListB)+b1-1)%(len(PointListB))])<=0:
            b1 = (len(PointListB)+b1-1)%(len(PointListB))
            done = False

    upperA = a1
    upperB = b1

    done = False
    a1 = rightMostPointA
    b1 = leftMostPointB
    while not done:

        a2 = (len(PointListA)+a1-1)%(len(PointListA))
        b2 = (b1 + 1)%(len(PointListB))
        
        done = True
        while clockwise(PointListA[a1], PointListB[b1], PointListB[(b1 + 1)%(len(PointListB))])>=0:
            b1 = (b1 + 1)%(len(PointListB))
    
            
        while clockwise(PointListB[b1], PointListA[a1], PointListA[(len(PointListA)+a1-1)%(len(PointListA))])<=0:
            a1 = (len(PointListA)+a1-1)%(len(PointListA))
            done = False


    lowerA = a1
    lowerB = b1

    mergeList = []
    mergeList.append(PointListA[upperA])
    print("upperA:", PointListA[upperA])
    print("lowerA:", PointListB[lowerB])
    while upperA != lowerA:
        upperA = (upperA+1)%len(PointListA)
        mergeList.append(PointListA[upperA])
    
    mergeList.append(PointListB[lowerB])
    while lowerB != upperB:
        lowerB = (lowerB+1)%len(PointListB)
        mergeList.append(PointListB[lowerB])
    
    return mergeList


def convexHull(pointList):
    if len(pointList) <= 5:
        return convexHullBase(pointList)
    
    left = pointList[0:len(pointList)//2]
    print(left)
    right = pointList[len(pointList)//2:]
    print(right)
    
    leftHull = convexHull(left)
    print(leftHull)
    rightHull = convexHull(right)    
    print(rightHull)


    return convexHullMerge(leftHull, rightHull)