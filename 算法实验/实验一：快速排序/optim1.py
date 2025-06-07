import re
import random
import time

# 随机基准
def PARTITION(A, p ,r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i =  i + 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1

def RANDOMIZED_PARTITION(A, p ,r):
    i = random.choice(range(p, r+1))
    A[i], A[r] = A[r], A[i]
    return PARTITION(A, p, r)

def RANDOMIZED_QUICKSORT(A, p, r):
    if p < r:
        q = RANDOMIZED_PARTITION(A, p, r)
        RANDOMIZED_QUICKSORT(A, p, q-1)
        RANDOMIZED_QUICKSORT(A, q+1, r)

# 三数取中

def MEDIAN_PARTITION(A, p, r):
    mid = (p + r) // 2
    # 对这三个数进行排序
    if A[p] > A[mid]:
        A[p], A[mid] = A[mid], A[p]
    if A[mid] > A[r]:
        A[mid], A[r] = A[r], A[mid]
    if A[p] > A[mid]:
        A[p], A[mid] = A[mid], A[p]
    A[mid], A[r - 1] = A[r - 1], A[mid]
    return PARTITION(A, p, r - 1)
    
def MEDIAN_QUICKSORT(A, p, r):
    if p < r:
        q = MEDIAN_PARTITION(A, p, r)
        MEDIAN_QUICKSORT(A, p, q-1)
        MEDIAN_QUICKSORT(A, q+1, r)

with open("data.txt", "r") as data_file:
    N, D = data_file.readlines()
    data = re.findall("\d+", D)
    N, A = int(N), [int(x) for x in data]

begin = time.time()
RANDOMIZED_QUICKSORT(A, 0, len(A) - 1)
out = time.time()
print(f"“随机基准”所花时间:{(out - begin) * 1000}毫秒")

with open("data.txt", "r") as data_file:
    N, D = data_file.readlines()
    data = re.findall("\d+", D)
    N, A = int(N), [int(x) for x in data]

begin = time.time()
MEDIAN_QUICKSORT(A, 0, len(A) - 1)
out = time.time()
print(f"“三数取中”所花时间:{(out - begin) * 1000}毫秒")

with open("sorted.txt", "w") as output_file:
    for num in A:
        output_file.write(str(num) + " ")