def gc(s):
    t = len(s) 
    g = s.count('G') 
    c = s.count('C') 
    p = ((g + c) / t) * 100 
    return p

s = "TGGATCCA"
print("GC content:", gc(s), "%")

def p(s):
    d = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}  
    c = ''.join(d[b] for b in s)  
    return s == c[::-1] 

s = "TGGATCCA"
if p(s):
    print(s, "это полиндром")
else:
    print(s, "это не полиндром")
