from math import sqrt

def distance(c1, c2):
    a = c1.x - c2.x
    b = c1.y - c2.y
    c = a ** 2 + b ** 2

    return sqrt(c)

def any(f, l):
    for x in l:
        if f(x):
            return True
    return False

def rotate_list(l, n = 1):
    newlist = l
    for x in range(n):
        newlist = list(zip(*newlist[::-1]))
    return newlist

def anyslice(i1,i2,l):
    s,e = (i1,i2) if i1 < i2 else (i2,i1)
    return l[s:e + 1]

def drop_first(f,l):
    for x in l:
        if f(x):
            l.remove(x)
            return

def between(i1,i2,l):
    """between(1,3,l) == between(3,1,l)"""
    if i1 < i2:
        return l[i1:i2]
    else:
        return l[i2:i1]
