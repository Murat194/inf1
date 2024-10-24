import math

def a(b):
    return sum(int(c) for c in str(b))

def d():
    e = 1
    while True:
        f = math.factorial(e)
        g = a(f)
        if f % g != 0:
            return e
        e += 1

# Пример использования
h = d()
print(f"Наименьшее положительное число n, факториал которого не делится нацело на сумму цифр самого факториала: {h}")
