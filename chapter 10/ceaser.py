def ceasar(a, b):
    t = ""
    for s in a:
      if s != ' ':
        s = s.lower()
        t += chr((ord(s) - ord('a') - b) % 26 + ord('a'))
      else:
        t += s
    return t

a = str(input("Шифр: "))
print("Дешифр:")
for b in range(26):
    t = ceasar(a, b)
    print(b, t)
