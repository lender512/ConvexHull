mid = (0,0)

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
    return not ((p[1]*q[0] < q[1]*p[0]))

def bubbleSort(arr):
    n = len(arr)
 
    for i in range(n-1):
 
        for j in range(0, n-i-1):
 
            if compare(arr[j], arr[j + 1]) :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

