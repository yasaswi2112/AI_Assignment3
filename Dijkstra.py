import csv
import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight):
        
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def load_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                u = row['Origin']
                v = row['Destination']
                w = float(row['Distance'])
                self.add_edge(u, v, w)

    def dijkstra(self, start):
        
        pq = []
        heapq.heappush(pq, (0, start))

        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        
        parent = {node: None for node in self.graph}

        while pq:
            current_dist, current_node = heapq.heappop(pq)

           
            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                distance = current_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parent[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return distances, parent

    def get_path(self, parent, target):
        path = []
        while target is not None:
            path.append(target)
            target = parent[target]
        return path[::-1]



if __name__ == "__main__":
    g = Graph()


    g.load_from_csv("india_roads.csv")

    start_city = input("Enter start city: ")

    distances, parent = g.dijkstra(start_city)

    print("\nShortest distances from", start_city, ":\n")

    for city in distances:
        print(f"{start_city} -> {city} = {distances[city]} km")

    
    target = input("\nEnter destination city to see path: ")
    path = g.get_path(parent, target)

    print("\nShortest path:")
    print(" -> ".join(path))
