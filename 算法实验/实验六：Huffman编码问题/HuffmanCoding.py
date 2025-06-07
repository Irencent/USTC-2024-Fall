import math
class Node():
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.code = None
        self.left = None
        self.right = None
        self.parent = None

def EXTRACT_MIN(Q):
    return Q.pop(0)

def INSERT(Q, x):
    i = 0
    while i < len(Q) and Q[i].freq < x.freq:
        i += 1
    Q.insert(i, x)

def HUFFMAN(C): # C 是一个包含 n 个节点的集合， 按照频率从小到大排序，有频率和字符两个属性
    n = len(C) 
    Q = [c for c in C]
    for i in range(n-1):
        z = Node(0)
        z.left = x = EXTRACT_MIN(Q)
        z.right = y = EXTRACT_MIN(Q)
        z.freq = x.freq + y.freq
        x.parent = y.parent = z
        INSERT(Q, z)
    return C

def HUFFMANCODING(C):
    C = HUFFMAN(C)
    for x in C:
        x.code = ''
        y = x
        while y.parent:
            if y.parent.left == y:
                x.code = '0' + x.code
            else:
                x.code = '1' + x.code
            y = y.parent
    return C

with open('orignal.txt', 'r') as f:
    text = f.read()
    freq = {}
    for c in text:
        if c != '\n' and c != ' ':
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1

C = [Node(freq[c], c) for c in freq]
C.sort(key=lambda x: x.freq)

# 计算定长编码总长度
fixed_length = math.ceil(math.log2(len(C))) * sum([c.freq for c in C])

# 求出 Huffman 编码
C = HUFFMANCODING(C)

# 计算Huffman编码总长度
huffman_length = sum([c.freq * len(c.code) for c in C])

# 计算压缩效率
compression_ratio = huffman_length / fixed_length
print('定长编码总长度：', fixed_length)
print('Huffman编码总长度：', huffman_length)
print('压缩效率：', compression_ratio)

# 输出编码表
to_write = []
to_write.append("字符\t频率\t编码\n")
for c in C:
    to_write.append(c.char + '\t' + str(c.freq) + '\t' + c.code + '\n')

with open('table.txt', 'w') as f:
    f.write(''.join(to_write))
