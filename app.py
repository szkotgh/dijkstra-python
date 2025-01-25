import json
import networkx as nx
import matplotlib.pyplot as plt
import heapq

class Graph:
    def __init__(self, map_file):
        with open(map_file, 'r') as file:
            data = json.load(file)
        print(f"nodes: {data['nodes']}")
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(data['nodes'])
        for edge in data['edges']:
            self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])

    def visualize(self, path=None):
        pos = nx.spring_layout(self.graph)
        weights = nx.get_edge_attributes(self.graph, 'weight')

        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='skyblue')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=weights)

        if path:
            edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(
                self.graph, pos, edgelist=edges_in_path, edge_color='red', width=2
            )

        plt.show()

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {node: None for node in self.graph.nodes}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor in self.graph.neighbors(current_node):
                weight = self.graph[current_node][neighbor]['weight']
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = end
        while current:
            path.append(current)
            current = previous_nodes[current]

        path.reverse()
        return path, distances[end]


if __name__ == "__main__":
    graph = Graph("map.json")

    start_node = input("Input start node: ").strip()
    end_node = input("Input end node: ").strip()

    path, cost = graph.dijkstra(start_node, end_node)
    print(f"Shortest path: {' -> '.join(path)}, cost: {cost}")

    graph.visualize(path)
