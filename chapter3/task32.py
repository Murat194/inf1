def f(s1, s2):
    if len(s1) != len(s2):
        return "Строки должны быть одинаковой длины"
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1    
    return distance

s1 = str(input())
s2 = str(input())

print("Расстояние ", s1, "и", s2, "равно", f)

