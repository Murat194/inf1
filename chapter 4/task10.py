from math import gcd
from functools import reduce
def a(b, c):
    return b * c // gcd(b, c)
def d(e):
    return reduce(a, e)
def f(g, h):
    i = len(h)
    j = sum(h)
    k = []
    for l in h:
        m = g - l
        if m <= 0:
            k.append(1)
        else:
            k.append(m / (g - j))    
    n = d(k)
    o = [int(p * n) for p in k]    
    q = reduce(gcd, o)
    o = [r // q for r in o]
    return o
print(f(3, [2, 1]))  
print(f(5, [1, 1, 2]))  
