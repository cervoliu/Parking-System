
import numpy as np
from functools import cmp_to_key

map = np.zeros((10, 10))
a = np.zeros((10, 10, 100))

class Cpoint():
    def __init__(self, x = 0, y = 0, t = 0):
        self.x = x
        self.y = y
        self.f = t
        self.t = 0
        self.g = 0
        self.h = 0
        self.parent = None
    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y
    def __lt__(self, other):
        return self.f <= other.f
    def __str__(self):
        return f'x={self.x} y={self.y}'
    def __repr__(self):
        return self.__str__()
class List():
    def __init__(self, parent ,next):
        self.parent = parent
        self.next = next

vec = []


def Exsit(vec, p):
    for cpoint in vec:
        if cpoint.x == p.x and cpoint.y == p.y:
            return True
    return False

def FindItem(vec, p):
    if Exsit(vec, p):
        for cpoint in vec:
            if cpoint.x == p.x and cpoint.y == p.y:
                return cpoint
        return None
    return None

def FindItemIter(vec, p):
    if Exsit(vec, p):
        for index, cpoint in enumerate(vec):
            if cpoint.x == p.x and cpoint.y == p.y:
                return index
        return len(vec) - 1
    return len(vec) - 1

def Score(beginner, ended ,cur):
    cur.g = abs(beginner.x - cur.x) + abs(beginner.y - cur.y)
    cur.h = abs(ended.x - cur.x) +abs(ended.y - cur.y)
    cur.f = cur.g + cur.h
    #print(f'g = {cur.g}')
    #print(f'h = {cur.h}')
    #print(f'f = {cur.f}')

def FindChildren(first, map, t, beginner, ended, open, close):
    bValid = False
    while True:
        if first.x - 1 >= 0 and map[first.x - 1][first.y] == 1 and a[first.x -1][first.y][t] != 0:
            left = Cpoint(first.x - 1, first.y, first.t + 1)
            Score(beginner, ended, left)
            if not Exsit(open, left) and not Exsit(close, left):
                left.parent = first
                open.append(left)
                bValid = True
            elif Exsit(open, left):
                old_open = FindItem(open, left)
                if left.f < old_open.f:
                    old_open.f = left.f
                    old_open.parent = first
            else:
                old_close = FindItem(close, left)
                if left.f < old_close.f:
                    old_close.f = left.f
                    old_close.parent = first
                    close.pop(FindItemIter(close, left))
                    open.append(left)

        if first.x + 1 <= 9 and map[first.x + 1][first.y] == 1 and a[first.x + 1][first.y][t] != 0:
            right = Cpoint(first.x + 1, first.y, first.t + 1)
            Score(beginner, ended, right)
            if not Exsit(open, right) and not Exsit(close, right):
                right.parent = first
                open.append(right)
                bValid = True
            elif Exsit(open, right):
                old_open = FindItem(open, right)
                if right.f < old_open.f:
                    old_open.f = right.f
                    old_open.parent = first
            else:
                old_close = FindItem(close, right)
                if right.f < old_close.f:
                    old_close.f = right.f
                    old_close.parent = first
                    close.pop(FindItemIter(close, right))
                    open.append(right)

        if first.y - 1 >= 0 and map[first.x][first.y - 1] == 1 and a[first.x][first.y - 1][t] != 0:
            bottom = Cpoint(first.x, first.y - 1, first.t + 1)
            Score(beginner, ended, bottom)
            if not Exsit(open, bottom) and not Exsit(close, bottom):
                bottom.parent = first
                open.append(bottom)
                bValid = True
            elif Exsit(open, bottom):
                old_open = FindItem(open, bottom)
                if bottom.f < old_open.f:
                    old_open.f = bottom.f
                    old_open.parent = first
            else:
                old_close = FindItem(close, bottom)
                if bottom.f < old_close.f:
                    old_close.f = bottom.f
                    old_close.parent = first
                    close.pop(FindItemIter(close, bottom))
                    open.append(bottom)

        if first.y + 1 <= 9 and map[first.x][first.y + 1] == 1 and a[first.x][first.y + 1][t] != 0:
            top = Cpoint(first.x, first.y + 1, first.t + 1)
            Score(beginner, ended, top)
            if not Exsit(open, top) and not Exsit(close, top):
                top.parent = first
                open.append(top)
                bValid = True
            elif Exsit(open, top):
                old_open = FindItem(open, top)
                if top.f < old_open.f:
                    old_open.f = top.f
                    old_open.parent = first
            else:
                old_close = FindItem(close, top)
                if top.f < old_close.f:
                    old_close.f = top.f
                    old_close.parent = first
                    close.pop(FindItemIter(close, top))
                    open.append(top)
        if bValid == False:
            first.t += 1
        else:
            break
    return bValid

def Mysort(p0, p1):
    if p0.f < p1.f:
        return -1
    else:
        return 1

def BestPath(beginner, ended, map):
    open = []
    close = []
    path = []
    bValidPoint = False
    open.append(beginner)
    while open:
        open.sort(key=cmp_to_key(Mysort))
        print(open)
        first = open[0]
        if first == ended:
            node = first
            path.clear()
            print(node.parent)
            while node.parent != None:
                path.append(node)
                node = node.parent
            return path
        close.append(first)
        open.pop(0)
        a[first.x][first.y][first.t] = 0
        bValidPoint = FindChildren(first, map, first.t, first, ended, open, close)
    return open
# //
# //if __name__ == '__main__':
# //    for i in range(10):
# //        for j in range(10):
# //            map[i][j] =  1
# //            for t in range(100):
# //                a[i][j][t] = 1
# //    map[0][4] = 0
# //    map[1][1] = 0
# //    map[1][5] = 0
# //    map[1][7] = 0
# //    map[2][6] = 0
# //    map[3][8] = 0
# //    map[4][6] = 0
# //    map[5][7] = 0
# //    map[6][3] = 0
# //    map[8][5] = 0
# //    map[8][6] = 0
# //    beginner = Cpoint(1, 5, 0)
# //    ended = Cpoint(9, 6, 10)
# //    path = BestPath(beginner, ended, map)
# //    p1 = path[0]
# //    for it in path:
# //        map[it.x][it.y] = 2
# //        i = p1.t - it.t
# //        for j in range(1,i+1):
# //           print(it.x, it.y)
# //        p1=it
