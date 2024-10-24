def move(zr):
    beg = 0
    for num in zr:
        if num != 0:
            zr[beg] = num
            beg += 1
    for i in range(beg, len(zr)):
        zr[i] = 0
    return zr
print(move([1, 0, 1, 2, 0, 1, 3]))
