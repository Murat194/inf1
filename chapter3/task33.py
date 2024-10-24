def f(n):

    if n % 2 == 0:
        result = 1
        for i in range(1, n//2 + 1):
            result *= 2 * i
    else:
        result = 1
        for i in range(1, (n + 1)//2 + 1):
            result *= (2 * i - 1)
    
    return result

n = int(input())
print(f(n))
