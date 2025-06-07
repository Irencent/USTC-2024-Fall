class Node:
    def __init__(self, key: int, right, left, parent, color: str):
        self.key = key
        self.right = right
        self.left = left
        self.parent = parent
        self.color = color

class REDBLACKTREE():
    # 初始化红黑树，除 nil 外无任何结点
    def __init__(self):
        self.nil = Node(None, None, None, None, 'black')
        self.root = self.nil
        self.write_lines = [] # 用于写输出的文件

    def RB_INSERT(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = 'RED'
        self.RB_INSERT_FIXUP(z)

    def LEFT_ROTATE(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RIGHT_ROTATE(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def RB_INSERT_FIXUP(self, z):
        while z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'RED':                    # case 1
                    print('Case 1')
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:             # case 2，将其转换为 case 3
                        print('Case 2')
                        z = z.parent
                        self.LEFT_ROTATE(z)
                    print('Case 3')
                    z.parent.color = 'BLACK'            # case 3
                    z.parent.parent.color = 'RED'
                    self.RIGHT_ROTATE(z.parent.parent)
            else:
                y = z.parent.parent.left                # 与上述情况完全对称
                if y.color == 'RED':                    # case 4
                    print('Case 4')
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:              # case 5，将其转换为 case 6
                        print('Case 5')
                        z = z.parent
                        self.RIGHT_ROTATE(z)
                    print('Case 6')
                    z.parent.color = 'BLACK'            # case 6
                    z.parent.parent.color = 'RED'
                    self.LEFT_ROTATE(z.parent.parent)
        self.root.color = 'BLACK'

    # 定义先序遍历输出函数
    def pre_order_traverse(self, file='NLR.txt'):
        node = self.root
        # 清空原有的 lines
        self.write_lines = []
        self.NLR(node)
        with open(file, 'w') as file:
            file.write(''.join(self.write_lines))
        file.close()

    def NLR(self, node):
        self.write_lines.append((str(node.key) if node!= self.nil else '#') + ', ' + node.color+'\n')
        if node.left != self.nil:
            self.NLR(node.left)
        if node.right != self.nil:
            self.NLR(node.right)

    # 定义中序遍历输出函数
    def in_order_traverse(self, file='LNR.txt'):
        node = self.root
        # 先清空原有的 lines
        self.write_lines = []
        self.LNR(node)
        with open(file, 'w') as file:
            file.write(''.join(self.write_lines))
        file.close()

    def LNR(self, node):
        if node.left != self.nil:
            self.LNR(node.left)
        self.write_lines.append((str(node.key) if node!= self.nil else '#') + ', ' + node.color + '\n')
        if node.right != self.nil:
            self.LNR(node.right)

    # 定义层次遍历输出函数
    def level_order_traverse(self, file='LOT.txt'):  # 层次遍历的结果保存在 LOT.txt 文件中
        # 先清空原有的 lines
        self.write_lines = []
        node = self.root
        NodeQueue = []
        NodeQueue.append(node)
        while NodeQueue:
            # 先推出队列第一个元素
            node = NodeQueue.pop(0)
            # 再将其左右孩子入队
            if node.left!= self.nil:
                NodeQueue.append(node.left)
            if node.right!= self.nil:
                NodeQueue.append(node.right)
            self.write_lines.append((str(node.key) if node!= self.nil else '#') + ', ' + node.color+'\n')
        with open(file, 'w') as file:
            file.write(''.join(self.write_lines))
        file.close()


with open('insert.txt', 'r') as file:
    N, keys = file.readlines()
    N, keys = int(N), [int(key) for key in keys.split()]

# 初始化一棵红黑树
T = REDBLACKTREE()

for key in keys:
    newnode = Node(key, None, None, None, 'RED')
    T.RB_INSERT(newnode)

# 先序、中序、层次遍历输出
T.pre_order_traverse()
T.in_order_traverse()
T.level_order_traverse()