"""
dm01 - 斐波拉契数
 
Author: poterliu
Version: 0.0.1
Date: 2026/10/26 
"""

def fib(n, caches: dict[int, int] = {1: 1, 2: 1}):
    if n < 2:
        return n
    if n in caches:
        return caches[n]
    caches[n] = fib(n-1) + fib(n-2)
    return caches[n]

if __name__ == '__main__':
    print(fib(100))
    print(fib(1000))