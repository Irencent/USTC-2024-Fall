import re
import time
def INSERTIONSORT(A, p, r):
    for i in range(p + 1, r + 1):
        key = A[i]
        j = i - 1
        while j >= p and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key

def PARTITION(A, p ,r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i =  i + 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1

def k_QUICKSORT(A, k, p, r):
    if abs(p - r) <= k:
        return INSERTIONSORT(A, p, r)
    if p < r:
        q = PARTITION(A, p, r)
        k_QUICKSORT(A, k, p, q-1)
        k_QUICKSORT(A, k, q+1, r)

with open("data.txt", "r") as data_file:
    N, D = data_file.readlines()
    data = re.findall("\d+", D)
    N, A = int(N), [int(x) for x in data]

begin = time.time()
k_QUICKSORT(A, 12, 0, len(A) - 1)
out = time.time()
print(f"所花时间:{(out - begin) * 1000}毫秒")

with open("sorted.txt", "w") as output_file:
    for num in A:
        output_file.write(str(num) + " ")
