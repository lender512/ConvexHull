from functools import cmp_to_key

mid = (0, 0)


def clockwise(a, b, c):
    result = (b[1]-a[1])*(c[0]-b[0]) - (c[1]-b[1])*(b[0]-a[0])
    if result == 0:
        return 0
    elif result > 0:
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


def Left_index(points):
     
    minn = 0
    for i in range(1,len(points)):
        if points[i][0] < points[minn][0]:
            minn = i
        elif points[i][0] == points[minn][0]:
            if points[i][1] > points[minn][1]:
                minn = i
    return minn

def convexHullBase(points):

    if len(points) < 3:
        return points
 
    # Find the leftmost point
    l = Left_index(points)
    
    hull = []
     
    p = l
    q = 0
    while(True):
         
        # Add current point to result
        hull.append(points[p])

        q = (p + 1) % len(points)
 
        for i in range(len(points)):
            if(clockwise(points[p],points[q], points[i]) == 1):
                q = i

        p = q

        if(p == l):
            break
    
    return hull

def convexHullMerge(PointListA, PointListB):
    
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
        
        done = True
        while clockwise(PointListB[b1], PointListA[a1], PointListA[(a1 + 1)%(len(PointListA))])>=0:
            print(PointListB[b1], PointListA[a1], PointListA[(a1 + 1)%(len(PointListA))])
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
    right = pointList[len(pointList)//2:]
    
    leftHull = convexHull(left)
    rightHull = convexHull(right)    


    return convexHullMerge(leftHull, rightHull)

