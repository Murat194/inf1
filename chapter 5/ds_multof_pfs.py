def ds_multof_pfs(nMin, nMax):
    def prime_factors(n):
        i = 2
        factors = []
        while i * i <= n:
            while (n % i) == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return factors

    def sum_of_divisors(n):
        divisors = [1, n]
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        return sum(divisors)
    result = []
    for num in range(nMin, nMax + 1):
        pfs = prime_factors(num)
        pfs_sum = sum(pfs)
        ds_sum = sum_of_divisors(num)
        if ds_sum % pfs_sum == 0:
            result.append(num)    
    return sorted(result)

print(ds_multof_pfs(10, 100))
print(ds_multof_pfs(20, 120))
