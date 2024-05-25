import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.colors import to_hex
import numpy as np
from task_4 import Node
from task_4 import add_edges
from task_4 import draw_tree


def bfs(root):
    if not root:
        return
    queue = deque([root])
    level = 0
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            node.color = to_hex(plt.cm.viridis(level / 10))
            draw_tree(root, f'BFS - Level {level}')
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level += 1

def dfs(node, level=0):
    if node is None:
        return
    node.color = to_hex(plt.cm.plasma(level / 10))
    draw_tree(node, f'DFS - Level {level}')
    dfs(node.left, level + 1)
    dfs(node.right, level + 1)

# Створення дерева
root = Node(0)
root.left = Node(1)
root.right = Node(2)
root.left.left = Node(3)
root.left.right = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)

print("Обхід в ширину (BFS):")
bfs(root)

print("Обхід в глибину (DFS):")
dfs(root)
