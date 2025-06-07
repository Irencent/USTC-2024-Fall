from bintrees import RBTree

def pre_order_traversal(node):
    if node is None:
        return
    # Visit the root (current node)
    print(f"Key: {node.key}")
    # Visit the left subtree
    pre_order_traversal(node.left)
    # Visit the right subtree
    pre_order_traversal(node.right)

def in_order_traversal(tree):
    for key, value in tree.items():
        print(f"Key: {key}")

from collections import deque

def level_order_traversal(tree):
    if tree._root is None:
        return
    
    queue = deque([tree._root])
    
    while queue:
        node = queue.popleft()
        print(f"Key: {node.key}")
        
        # Enqueue left child
        if node.left is not None:
            queue.append(node.left)
        # Enqueue right child
        if node.right is not None:
            queue.append(node.right)


T = RBTree()
with open('insert.txt', 'r') as file:
    N, keys = file.readlines()
    N, keys = int(N), [int(key) for key in keys.split()]

for key in keys:
    T.insert(key,'')


print("Pre-order Traversal:")
pre_order_traversal(T._root)

print("\nIn-order Traversal:")
in_order_traversal(T)

print("\nLevel-order Traversal:")
level_order_traversal(T)

