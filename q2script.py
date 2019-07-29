import math
import heapq
import numpy

def estimate(x,y,a,b,n):
    return math.ceil(math.sqrt((n-x-1)**2+(n-y-1)**2)/math.sqrt(a**2+b**2))

def moves(x,y,a,b,n):
    return [x for x in [(x+a,y+b),(x+a,y-b),(x-a,y+b),(x-a,y-b),(x+b,y+a),(x+b,y-a),(x-b,y+a),(x-b,y-a)] if
            x[0]>=0 and x[1]>=0 and x[0]<n and x[1]<n]

def findpath(a,b,n):
    heap=[(estimate(0,0,a,b,n),(0,0))]
    distarray=-numpy.ones((n,n),numpy.int16)
    distarray[(0,0)]=0
    xfromarray=-numpy.ones((n,n),numpy.int16)
    yfromarray=-numpy.ones((n,n),numpy.int16)
    while distarray[n-1][n-1]<0 and len(heap)>0:
        x=heapq.heappop(heap)[1]
        for m in moves(x[0],x[1],a,b,n):
            if distarray[m]<0:
                distarray[m]=distarray[x]+1
                xfromarray[m]=x[0]
                yfromarray[m]=x[1]
                heapq.heappush(heap,(estimate(m[0],m[1],a,b,n)+distarray[m],m))
    if distarray[(n-1,n-1)]<0:
        raise ValueError('No path for knight({},{}) on board size {}'.format(a,b,n))
    else:
        result=[]
        x=(n-1,n-1)
        while x!=(0,0):
            newx=xfromarray[x]
            newy=yfromarray[x]
            x=(newx,newy)
            result.append(x)
        return result

if __name__=="__main__":
    #q1
    print("Q1")
    print(len(findpath(1,2,5)))
    #q2
    print("Q2")
    total=0
    for b in range(1,5):
        for a in range(1,b+1):
            try:
                findpath(a,b,5)
            except ValueError:
                total=total+1
    print(total)
    #q3
    print("Q3")
    total=0
    for b in range(1,5):
        for a in range(1,b+1):
            try:
                total=total+len(findpath(a,b,5))
            except ValueError:
                pass
    print(total)
    #q4
    print("Q4")
    print(len(findpath(4,7,25)))
    #q5
    print("Q5")
    total=0
    for b in range(1,25):
        for a in range(1,b+1):
            try:
                findpath(a,b,25)
            except ValueError:
                total=total+1
    print(total)
    #q6
    print("Q6")
    total=0
    for b in range(1,25):
        for a in range(1,b+1):
            try:
                total=total+len(findpath(a,b,25))
            except ValueError:
                pass
    print(total)
    #q7
    print("Q7")
    print(len(findpath(13,23,1000)))
    #q8
    print("Q8")
    print(len(findpath(73,101,10000)))