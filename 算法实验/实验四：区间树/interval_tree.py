import re
class Node:
    def __init__(self, low, high, right, left, parent, color: str):
        # 以低端点为序插入节点
        self.key = low
        self.low = low
        self.high = high
        self.right = right
        self.max = high  # Initialize max as the high value of the node
        self.left = left
        self.parent = parent
        self.color = color

class INTERVALTREE():
    # 初始化红黑树，除 nil 外无任何结点
    def __init__(self):
        self.nil = Node(None, None, None, None, None, 'black')
        self.nil.max = float('-inf')  # Max of nil is negative infinity
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
        self.UPDATE_MAX(z)  # Update the max attributes

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
        # Update max attributes
        self.UPDATE_MAX(x)
        self.UPDATE_MAX(y)

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
        # Update max attributes
        self.UPDATE_MAX(y)
        self.UPDATE_MAX(x)

    def RB_INSERT_FIXUP(self, z):
        while z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'RED':                    # case 1
                    # print('Case 1')
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:             # case 2，将其转换为 case 3
                        # print('Case 2')
                        z = z.parent
                        self.LEFT_ROTATE(z)
                    # print('Case 3')
                    z.parent.color = 'BLACK'            # case 3
                    z.parent.parent.color = 'RED'
                    self.RIGHT_ROTATE(z.parent.parent)
            else:
                y = z.parent.parent.left                # 与上述情况完全对称
                if y.color == 'RED':                    # case 4
                    #print('Case 4')
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:              # case 5，将其转换为 case 6
                        #print('Case 5')
                        z = z.parent
                        self.RIGHT_ROTATE(z)
                    #print('Case 6')
                    z.parent.color = 'BLACK'            # case 6
                    z.parent.parent.color = 'RED'
                    self.LEFT_ROTATE(z.parent.parent)
        self.root.color = 'BLACK'
    
    def UPDATE_MAX(self, node):
        while node != self.nil:
            node.max = max(
                node.high,
                node.left.max if node.left != self.nil else float('-inf'),
                node.right.max if node.right != self.nil else float('-inf')
            )
            node = node.parent

    def INTERVAL_SEARCH(self, i):
        x = self.root
        while x != self.nil and not (x.low <= i[1] and x.high >= i[0]):
            if x.left != self.nil and x.left.max >= i[0]:
                x = x.left
            else:
                x = x.right
        return (x.low, x.high)
    

# 初始化一棵红黑树
T = INTERVALTREE()

# 读取文件
with open('insert.txt', 'r') as file:
    N_intervals = file.readlines()
    N_intervals.pop(0)
    for interval in N_intervals:
        low, high = [int(x) for x in interval.split()]
        newnode = Node(low, high, None, None, None, 'RED')
        T.RB_INSERT(newnode)

intervals_to_search = [[100, 234], [32, 35], [17, 19], [60, 63], [39, 43]]
for i in intervals_to_search:
    print(f"对于示例{i},结果为:{T.INTERVAL_SEARCH(i)}")

i = input()
while i:
    low, high = [int(x) for x in i.split()]
    print(T.INTERVAL_SEARCH((low, high)))
    i = input()

