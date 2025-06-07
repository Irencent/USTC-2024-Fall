P = []
with open("data.txt", "r") as points_file:
    points = points_file.readlines()
    for point in points:
        item, x, y = re.findall(r"[\-\d\.]+", point)
        P.append((float(x), float(y), int(item)))

# 计算两点的欧几里得距离
def distance(x, y): 
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

delta = distance(P[0], P[1])
pair = (P[0][2], P[1][2])

for i in range(len(P)):
    for j in range(i + 1, len(P)):
        delta0 = distance(P[i], P[j])
        if delta0 < delta:
            delta = delta0
            pair = (P[i][2], P[j][2])

