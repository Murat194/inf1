m = []
for i in range(10):
    m.append(i)
number = int(input())
for part in m:
    print(str(number) + " * " + str(part) + " = " + str(number * part))
