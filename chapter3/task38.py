def f(n):
    n = n.replace(" ", "")
    a = n[::-1]
    b = 0
    for i in range(len(a)):
        c = int(a[i])
        if i % 2 == 1:
            c *= 2
            if c > 9:
                c -= 9
        b += c
    return b % 10 == 0

n = '4799 2739 8713 6272'
print(f(n))
