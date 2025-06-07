import re
import time
def AGGREGATE_PARTITION(A, p, r):
    x = A[r]
    i = p - 1
    sup = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i =  i + 1
            A[i], A[j] = A[j], A[i]
            if A[i] == x:
                sup = sup + 1
                A[sup], A[i] = A[i], A[sup]
    A[i + 1], A[r] = A[r], A[i + 1]
    # 将与基准相等的元素聚集在一起
    if sup >= p:
        for k in range(p, sup + 1):
            A[k], A[i + k - sup] = A[i + k - sup], A[k]
    return i + p - sup, i + 1

def AGGREGATE_QUICKSORT(A, p, r):
    if p < r:
        l, q = AGGREGATE_PARTITION(A, p, r)
        AGGREGATE_QUICKSORT(A, p, l-1)
        AGGREGATE_QUICKSORT(A, q+1, r)

with open("data.txt", "r") as data_file:
    N, D = data_file.readlines()
    data = re.findall("\d+", D)
    N, A = int(N), [int(x) for x in data]

begin = time.time()
AGGREGATE_QUICKSORT(A, 0, len(A) - 1)
out = time.time()
print(f"“聚集元素”所花时间:{(out - begin) * 1000}毫秒")

with open("sorted.txt", "w") as output_file:
    for num in A:
        output_file.write(str(num) + " ")
