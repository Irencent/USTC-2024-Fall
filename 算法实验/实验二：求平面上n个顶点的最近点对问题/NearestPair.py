import re
import time
# 计算两点的欧几里得距离
def distance(x, y): 
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

def NEARESTPAIR(P, X, Y):
    # 递归终止条件
    if len(P) <= 3:
        delta = distance(P[0], P[1])
        pair = (P[0][2], P[1][2])
        for i in range(len(P)):
            for j in range(i+1, len(P)):
                if delta > distance(P[i], P[j]):
                    pair = (P[i][2], P[j][2])
                    delta = distance(P[i], P[j])
        return pair, delta

    
    # 产生 P, X 的子集
    PL, PR = P[:(len(P)-1)//2+1], P[(len(P)-1)//2+1:]
    XL, XR = X[:(len(X)-1)//2+1], X[(len(P)-1)//2+1:]

    # 产生 Y 的子集
    YL, YR = [], []
    for y in Y:
        if y in PL:
            YL.append(y)
        else:
            YR.append(y)
    
    # 两次递归调用
    pairL, deltaL = NEARESTPAIR(PL, XL, YL)
    pairR, deltaR = NEARESTPAIR(PR, XR, YR)
    pair, delta = (pairL, deltaL) if deltaL < deltaR else (pairR, deltaR)

    # 计算两点分别在两边的情况
    Y0 = [] # 产生 Y'
    for y in Y:
        if abs(y[0] - P[(len(P)-1)//2][0]) < delta:
            Y0.append(y)

    for i in range(len(Y0)):
        for j in range(7):
            if i + j + 1 < len(Y0):
                delta0 = distance(Y0[i], Y0[i + j + 1])
                if delta0 < delta:
                    delta = delta0
                    pair = (Y0[i][2], Y0[i + j + 1][2])

    return pair, delta

def BRUTEFORCE(P):
    delta = distance(P[0], P[1])
    pair = (P[0][2], P[1][2])

    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            delta0 = distance(P[i], P[j])
            if delta0 < delta:
                delta = delta0
                pair = (P[i][2], P[j][2])
    
    return pair, delta


P, X, Y = [], [], []
with open("data.txt", "r") as points_file:
    points = points_file.readlines()
    for point in points:
        item, x, y = re.findall(r"[\-\d\.]+", point)
        P.append((float(x), float(y), int(item)))
        X.append((float(x), float(y), int(item)))
        Y.append((float(x), float(y), int(item)))

# presort the points
P = sorted(P, key=lambda x: x[0])
X = sorted(X, key=lambda x: x[0])
Y = sorted(Y, key=lambda x: x[1])

begin = time.time()
pair, delta = NEARESTPAIR(P, X, Y)
out = time.time()
print("通过分治算法得到的结果为：", pair, delta)
print(f"分治算法所花时间为:{(out - begin) * 1000}毫秒")

begin = time.time()
pair, delta = BRUTEFORCE(P)
out = time.time()
print("通过暴力搜索算法得到的结果为：", pair, delta)
print(f"分治算法所花时间为:{(out - begin) * 1000}毫秒")
