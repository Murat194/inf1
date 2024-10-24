def bytes(x):
    return x * 1024

def kilobytes(x):
    return x / 1024

a = int(input())
print("Из кб в б:", bytes(a), ". Из б в кб", kilobytes(a))

