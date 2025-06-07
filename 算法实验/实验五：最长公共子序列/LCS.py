def LCS_LENGTH(X, Y):
    m = len(X)
    n = len(Y)
    b = [[0 for i in range(n+1)] for j in range(m+1)]
    c = [[0 for i in range(n+1)] for j in range(m+1)]
    for i in range(1, m+1):
        c[i][0] = 0
    for j in range(n+1):
        c[0][j] = 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = '↖'
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = '↑'
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = '←'
    return c, b

def LCS_LENGTH_UPDATE_1(X, Y):
    if len(X) < len(Y):
        X, Y = Y, X
    m = len(X)
    n = len(Y)
    c = [[0 for i in range(n+1)] for j in range(2)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                c[1][j] = c[0][j-1] + 1
            elif c[0][j] >= c[1][j-1]:
                c[1][j] = c[0][j]
            else:
                c[1][j] = c[1][j-1]
        c[0] = c[1]
    print("(时间复杂度为 2 * O(min(m, n)))LCS长度：", c[1][n])

def LCS_LENGTH_UPDATE_2(X, Y):
    if len(X) < len(Y):
        X, Y = Y, X
    m = len(X)
    n = len(Y)
    c = [0 for i in range(n+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                c[j] = c[j-1] + 1
            elif c[j-1] >= c[j]:
                c[j] = c[j-1]
            else:
                c[j] = c[j]
    print("(时间复杂度为O(min(m, n)))LCS长度：", c[n])

def PRINT_LCS(b, X, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == '↖':
        PRINT_LCS(b, X, i-1, j-1)
        print(X[i-1], end='')
    elif b[i][j] == '↑':
        PRINT_LCS(b, X, i-1, j)
    else:
        PRINT_LCS(b, X, i, j-1)


'''X = 'ABCBDAB'
Y = 'BDCAB'
c, b = LCS_LENGTH(X, Y)
print("LCS:",end='')
PRINT_LCS(b, X, len(X), len(Y))
print("，长度：", c[len(X)][len(Y)])'''

while True:
    X = input("请输入第一个字符串：")
    Y = input("请输入第二个字符串：")
    LCS_LENGTH_UPDATE_1(X, Y)
    LCS_LENGTH_UPDATE_2(X, Y)
    c, b = LCS_LENGTH(X, Y)
    print("LCS:",end='')
    PRINT_LCS(b, X, len(X), len(Y))
    print("，长度：", c[len(X)][len(Y)])
    if input("输入0退出，输入其他继续：") == '0':
        break
