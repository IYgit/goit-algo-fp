"""
Завдання 4. Візуалізація піраміди (бінарної купи)

Базовий код для відображення бінарних дерев взято з умови завдання.
Додано функцію build_heap_tree(), яка перетворює масив-купу
на дерево вузлів Node, та функцію draw_heap(), яка будує і відображає
бінарну купу (min-heap або max-heap) через networkx + matplotlib.
"""

import heapq
import uuid

import networkx as nx
import matplotlib.pyplot as plt


# ── Базовий код з умови завдання ──────────────────────────────────────────────

class Node:
    def __init__(self, key, color="skyblue"):
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
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title: str = "Binary Tree"):
    tree = nx.DiGraph()
    pos  = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=14)
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, font_size=11, font_weight="bold")
    plt.tight_layout()
    plt.show()


# ── Нова функція: побудова бінарної купи ──────────────────────────────────────

def build_heap_tree(heap_array: list) -> Node:
    """
    Перетворює масив-представлення бінарної купи на дерево вузлів Node.

    У бінарній купі (масив з індексами 0..n-1):
        лівий нащадок  вузла i  →  2*i + 1
        правий нащадок вузла i  →  2*i + 2

    Кольори вузлів:
        корінь         — золотий   (#FFC300)
        внутрішні вузли — блакитний (#87CEEB)
        листки          — зелений   (#90EE90)

    Args:
        heap_array: список елементів у порядку, що відповідає бінарній купі.

    Returns:
        Корінь побудованого дерева (Node).
    """
    if not heap_array:
        raise ValueError("Масив купи не може бути порожнім.")

    n     = len(heap_array)
    nodes = [Node(val) for val in heap_array]

    # Визначаємо кольори
    for i, node in enumerate(nodes):
        left_idx  = 2 * i + 1
        right_idx = 2 * i + 2
        is_leaf   = (left_idx >= n) and (right_idx >= n)

        if i == 0:
            node.color = "#FFC300"   # корінь — золотий
        elif is_leaf:
            node.color = "#90EE90"   # листок — зелений
        else:
            node.color = "#87CEEB"   # внутрішній — блакитний

    # Зв'язуємо вузли
    for i, node in enumerate(nodes):
        left_idx  = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < n:
            node.left  = nodes[left_idx]
        if right_idx < n:
            node.right = nodes[right_idx]

    return nodes[0]


def draw_heap(data: list, heap_type: str = "min") -> None:
    """
    Будує бінарну купу з довільного списку та відображає її.

    Args:
        data      : вхідний список чисел
        heap_type : "min" — мінімальна купа (за замовчуванням),
                    "max" — максимальна купа
    """
    if heap_type == "max":
        heap_array = [-x for x in data]
        heapq.heapify(heap_array)
        heap_array = [-x for x in heap_array]   # повертаємо оригінальні значення
        title = "Максимальна бінарна купа (Max-Heap)"
    else:
        heap_array = list(data)
        heapq.heapify(heap_array)
        title = "Мінімальна бінарна купа (Min-Heap)"

    print(f"\n{title}")
    print(f"  Масив купи: {heap_array}")

    root = build_heap_tree(heap_array)
    draw_tree(root, title=title)


# ── Демонстрація ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = [15, 3, 10, 7, 1, 9, 4, 12, 6, 2]

    print("Вхідні дані:", data)

    # Min-Heap
    draw_heap(data, heap_type="min")

    # Max-Heap
    draw_heap(data, heap_type="max")

