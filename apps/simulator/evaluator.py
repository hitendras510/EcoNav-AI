import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_city(self, city):
        if city not in self.graph:
            self.graph[city] = []

    def add_road(self, city1, city2, distance, pollution):
        self.add_city(city1)
        self.add_city(city2)
        # Undirected graph
        self.graph[city1].append((city2, distance, pollution))
        self.graph[city2].append((city1, distance, pollution))

    def show_graph(self):
        for city in self.graph:
            print(f"{city} -> {self.graph[city]}")


class Routing:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, end, mode="distance"):
        pq = [(0, start, [])]  # (cost, current_node, path)
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue

            path = path + [node]
            visited.add(node)

            if node == end:
                return cost, path

            for neighbor, distance, pollution in self.graph[node]:
                if neighbor not in visited:
                    if mode == "distance":
                        new_cost = cost + distance
                    elif mode == "eco":
                        new_cost = cost + pollution
                    else:
                        raise ValueError("Invalid mode selected")

                    heapq.heappush(pq, (new_cost, neighbor, path))

        return float("inf"), []


# ---------------- SAMPLE DATA ----------------
g = Graph()

g.add_road("A", "B", 5, 10)
g.add_road("A", "C", 8, 3)
g.add_road("B", "D", 2, 2)
g.add_road("C", "D", 4, 6)
g.add_road("C", "E", 7, 1)
g.add_road("D", "E", 1, 2)
g.add_road("D", "F", 6, 8)
g.add_road("E", "F", 3, 1)

router = Routing(g.graph)

# ---------------- CLI ----------------
print("\nAvailable Cities:", list(g.graph.keys()))

start = input("Enter source city: ").strip()
end = input("Enter destination city: ").strip()

if start not in g.graph or end not in g.graph:
    print("❌ Invalid city name")
    exit()

print("\nChoose Mode:")
print("1 → Shortest Distance")
print("2 → Eco-Friendly Route")

choice = input("Enter choice: ").strip()

if choice == "1":
    cost, path = router.dijkstra(start, end, mode="distance")
    print("\n✅ Shortest Distance Route:")
elif choice == "2":
    cost, path = router.dijkstra(start, end, mode="eco")
    print("\n🌱 Eco-Friendly Route:")
else:
    print("❌ Invalid choice")
    exit()

if path:
    print("Path:", " → ".join(path))
    print("Total Cost:", cost)
else:
    print("No route found")