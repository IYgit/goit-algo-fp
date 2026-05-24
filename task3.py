"""
Завдання 3. Дерева, алгоритм Дейкстри

Реалізація алгоритму Дейкстри для знаходження найкоротших шляхів
у зваженому графі з використанням бінарної купи (heapq).

Структура:
  - WeightedGraph   — зважений орієнтований граф (список суміжності)
  - dijkstra()      — алгоритм Дейкстри на бінарній купі
  - reconstruct_path() — відновлення конкретного шляху
  - main()          — демонстрація на тестовому графі
"""

import heapq
from typing import Optional


# ── Граф ─────────────────────────────────────────────────────────────────────

class WeightedGraph:
    """Зважений орієнтований граф на основі словника списків суміжності."""

    def __init__(self):
        self._adj: dict[str, list[tuple[str, float]]] = {}

    def add_vertex(self, v: str) -> None:
        """Додає вершину (якщо її ще немає)."""
        if v not in self._adj:
            self._adj[v] = []

    def add_edge(self, u: str, v: str, weight: float, bidirectional: bool = False) -> None:
        """
        Додає ребро u → v з вагою weight.
        Якщо bidirectional=True, додає також v → u.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].append((v, weight))
        if bidirectional:
            self._adj[v].append((u, weight))

    @property
    def vertices(self) -> list[str]:
        return list(self._adj.keys())

    def neighbors(self, v: str) -> list[tuple[str, float]]:
        """Повертає список (сусід, вага) для вершини v."""
        return self._adj.get(v, [])


# ── Алгоритм Дейкстри ─────────────────────────────────────────────────────────

def dijkstra(graph: WeightedGraph,
             start: str) -> tuple[dict[str, float], dict[str, Optional[str]]]:
    """
    Алгоритм Дейкстри з бінарною купою (min-heap).

    Args:
        graph : зважений граф
        start : початкова вершина

    Returns:
        distances : словник {вершина → найкоротша відстань від start}
        previous  : словник {вершина → попередня вершина у найкоротшому шляху}
                    (потрібен для відновлення шляху)
    """
    INF = float("inf")

    # Ініціалізація: відстань до всіх вершин = ∞
    distances: dict[str, float] = {v: INF for v in graph.vertices}
    distances[start] = 0.0

    previous: dict[str, Optional[str]] = {v: None for v in graph.vertices}

    # Бінарна купа: (відстань, вершина)
    heap: list[tuple[float, str]] = [(0.0, start)]

    visited: set[str] = set()

    while heap:
        current_dist, current_v = heapq.heappop(heap)  # витягуємо вершину з мін. відстанню

        if current_v in visited:
            # Стара (застаріла) запис у купі — пропускаємо
            continue
        visited.add(current_v)

        for neighbor, weight in graph.neighbors(current_v):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_v
                heapq.heappush(heap, (new_dist, neighbor))  # додаємо у купу

    return distances, previous


def reconstruct_path(previous: dict[str, Optional[str]],
                     start: str,
                     end: str) -> list[str]:
    """
    Відновлює найкоротший шлях від start до end за словником previous.

    Returns:
        Список вершин від start до end (або порожній список, якщо шляху немає).
    """
    path: list[str] = []
    current: Optional[str] = end

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    if path[0] != start:
        return []   # шляху не існує
    return path


# ── Демонстрація ──────────────────────────────────────────────────────────────

def main() -> None:
    """
    Тестовий зважений граф:

        A --4-- B --1-- C
        |       |       |
        2       3       5
        |       |       |
        D --8-- E --2-- F
    """
    g = WeightedGraph()
    edges = [
        ("A", "B", 4),
        ("A", "D", 2),
        ("B", "C", 1),
        ("B", "E", 3),
        ("C", "F", 5),
        ("D", "E", 8),
        ("E", "F", 2),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w, bidirectional=True)

    start_vertex = "A"
    distances, previous = dijkstra(g, start_vertex)

    print("=" * 50)
    print(f"  Алгоритм Дейкстри  (початкова вершина: {start_vertex})")
    print("=" * 50)

    print(f"\n{'Вершина':<10} {'Відстань':<12} {'Найкоротший шлях'}")
    print("-" * 50)
    for vertex in sorted(distances):
        dist = distances[vertex]
        path = reconstruct_path(previous, start_vertex, vertex)
        path_str = " → ".join(path) if path else "недосяжна"
        dist_str = str(dist) if dist != float("inf") else "∞"
        print(f"{vertex:<10} {dist_str:<12} {path_str}")

    print("=" * 50)


if __name__ == "__main__":
    main()

