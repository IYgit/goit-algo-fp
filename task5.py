"""
Завдання 5. Візуалізація обходу бінарного дерева

Програма будує бінарне дерево (з купи), а потім крок за кроком
відображає порядок обходу вузлів:
  - DFS (у глибину) — через стек (без рекурсії)
  - BFS (у ширину) — через чергу (без рекурсії)

Кожен вузол при відвідуванні отримує унікальний колір,
що плавно переходить від темного до світлого відповідно
до порядку обходу (16-кова RGB нотація, наприклад #1296F0).
"""

import uuid
import heapq
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ── Вузол та базові функції з завдання 4 ─────────────────────────────────────

class Node:
    def __init__(self, key, color: str = "skyblue"):
        self.left  = None
        self.right = None
        self.val   = key
        self.color = color
        self.id    = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def build_heap_tree(heap_array: list) -> Node:
    """Перетворює масив-купу на дерево вузлів Node."""
    if not heap_array:
        raise ValueError("Масив купи порожній.")
    n     = len(heap_array)
    nodes = [Node(val) for val in heap_array]
    for i, node in enumerate(nodes):
        if 2 * i + 1 < n:
            node.left  = nodes[2 * i + 1]
        if 2 * i + 2 < n:
            node.right = nodes[2 * i + 2]
    return nodes[0]


# ── Генерація кольорів ────────────────────────────────────────────────────────

def generate_colors(n: int,
                    dark: tuple  = (18,  150, 240),    # #1296F0 — темний
                    light: tuple = (200, 230, 255)) -> list[str]:
    """
    Повертає список із n HEX-кольорів, що плавно переходять
    від темного до світлого (відповідно до порядку обходу).
    """
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)   # 0.0 (перший) → 1.0 (останній)
        r = int(dark[0] + (light[0] - dark[0]) * t)
        g = int(dark[1] + (light[1] - dark[1]) * t)
        b = int(dark[2] + (light[2] - dark[2]) * t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


# ── Обходи (без рекурсії) ─────────────────────────────────────────────────────

def dfs_order(root: Node) -> list[Node]:
    """
    Обхід у глибину (DFS) через явний стек.
    Порядок: корінь → ліве піддерево → праве піддерево (pre-order).
    """
    if root is None:
        return []
    order: list[Node] = []
    stack: list[Node] = [root]
    while stack:
        node = stack.pop()          # LIFO → стек
        order.append(node)
        if node.right:              # правий кладемо першим, щоб лівий виймався раніше
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_order(root: Node) -> list[Node]:
    """
    Обхід у ширину (BFS) через чергу.
    Порядок: рівень за рівнем, зліва направо.
    """
    if root is None:
        return []
    order: list[Node] = []
    queue: deque[Node] = deque([root])
    while queue:
        node = queue.popleft()      # FIFO → черга
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


# ── Відображення ──────────────────────────────────────────────────────────────

def draw_traversal(root: Node,
                   visit_order: list[Node],
                   title: str) -> None:
    """
    Малює дерево, де кожен вузол забарвлений відповідно
    до порядку його відвідування (темний → світлий).
    """
    colors_list = generate_colors(len(visit_order))

    # Присвоюємо кольори вузлам
    color_map: dict[str, str] = {}
    for step, node in enumerate(visit_order):
        node.color     = colors_list[step]
        color_map[node.id] = colors_list[step]

    # Будуємо граф
    graph = nx.DiGraph()
    pos   = {root.id: (0, 0)}
    graph = add_edges(graph, root, pos)

    node_colors = [color_map.get(n, "#CCCCCC") for n in graph.nodes()]
    labels      = {n: graph.nodes[n]["label"] for n in graph.nodes()}

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_title(title, fontsize=14, fontweight="bold")
    nx.draw(graph, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=node_colors,
            font_size=10, font_weight="bold", ax=ax)

    # Легенда: номер кроку → колір
    patches = [
        mpatches.Patch(color=colors_list[i],
                       label=f"Крок {i + 1}: вузол {visit_order[i].val}")
        for i in range(len(visit_order))
    ]
    ax.legend(handles=patches, loc="upper left",
              bbox_to_anchor=(1.01, 1), borderaxespad=0,
              fontsize=9, title="Порядок відвідування")

    plt.tight_layout()
    plt.show()


# ── Головна функція ───────────────────────────────────────────────────────────

def main() -> None:
    data = [0, 4, 1, 5, 10, 3, 2, 7, 8, 6]
    heap = list(data)
    heapq.heapify(heap)

    print(f"Вхідні дані : {data}")
    print(f"Min-Heap    : {heap}")

    # ── DFS ──
    root_dfs = build_heap_tree(heap)
    order_dfs = dfs_order(root_dfs)
    print("\nDFS (у глибину, pre-order):", [n.val for n in order_dfs])
    draw_traversal(root_dfs, order_dfs,
                   "DFS — обхід у глибину (стек, pre-order)\n"
                   "Темний = перший відвіданий, Світлий = останній")

    # ── BFS ──
    root_bfs = build_heap_tree(heap)
    order_bfs = bfs_order(root_bfs)
    print("BFS (у ширину)          :", [n.val for n in order_bfs])
    draw_traversal(root_bfs, order_bfs,
                   "BFS — обхід у ширину (черга)\n"
                   "Темний = перший відвіданий, Світлий = останній")


if __name__ == "__main__":
    main()

