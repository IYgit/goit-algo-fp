import heapq

class Graph:
    def __init__(self):
        self.edges = {}
        self.nodes = set()
    
    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))
        self.nodes.add(from_node)
        self.nodes.add(to_node)

def dijkstra(graph, start):
    # Ініціалізація мін-кучі
    heap = []
    heapq.heappush(heap, (0, start))
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}
    
    while heap:
        current_distance, current_node = heapq.heappop(heap)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph.edges.get(current_node, []):
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))
    
    return distances, previous_nodes

def shortest_path(previous_nodes, start, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()
    if path[0] == start:
        return path
    return []

# TEST
if __name__ == "__main__":
    graph = Graph()
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('C', 'D', 1)
    graph.add_edge('B', 'D', 5)

    start_node = 'A'
    distances, previous_nodes = dijkstra(graph, start_node)

    print("Відстані від початкової вершини:")
    for node in distances:
        print(f"Відстань від {start_node} до {node}: {distances[node]}")

    target_node = 'D'
    path = shortest_path(previous_nodes, start_node, target_node)
    print(f"Найкоротший шлях від {start_node} до {target_node}: {path}")
