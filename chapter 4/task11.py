MOD = 1000000007

def binomial_coefficients(max_k):
    C = [[0] * (max_k + 1) for _ in range(max_k + 1)]
    for i in range(max_k + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    return C

def apply_queries(n, m, a, queries):
    max_k = max(k for _, _, k in queries)
    C = binomial_coefficients(max_k)
    changes = [[0] * (max_k + 1) for _ in range(n + 1)]
    for l, r, k in queries:
        for d in range(k + 1):
            changes[l - 1][d] = (changes[l - 1][d] + C[k][d]) % MOD
            if r < n:
                changes[r][d] = (changes[r][d] - C[k][d] * pow(r - l + k - d + 1, MOD - 2, MOD)) % MOD
    for i in range(n):
        for d in range(max_k, 0, -1):
            changes[i + 1][d - 1] = (changes[i + 1][d - 1] + changes[i][d] * (i + 1)) % MOD
            changes[i][d - 1] = (changes[i][d - 1] + changes[i][d]) % MOD
        a[i] = (a[i] + changes[i][0]) % MOD
    
    return a
n, m = 5, 1
a = [0, 0, 0, 0, 0]
queries = [(1, 5, 0)]
result = apply_queries(n, m, a, queries)
print(' '.join(map(str, result)))

n, m = 10, 2
a = [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
queries = [(1, 6, 1), (6, 10, 2)]
result = apply_queries(n, m, a, queries)
print(' '.join(map(str, result)))
