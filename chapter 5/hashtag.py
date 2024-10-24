def f(s):
    words = s.split()
    hashtag = '#' + ''.join(word.capitalize() for word in words)
    if len(hashtag) > 140 or len(hashtag) == 1:
        return False
    return hashtag

s = str(input())
print(f(s))
