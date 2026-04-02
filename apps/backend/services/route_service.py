from apps.backend.services.eco_route_model import choose_best_neighbor
from apps.backend.services import graph_store
from apps.simulator.evaluator import Graph, RLEnv, get_route
from packages.shared.utils import percent_improvement


# =====================
# HELPERS
# =====================
def compute_exposure(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for n, dist, pol in graph.get_neighbors(path[i]):
            if n == path[i + 1]:
                total += dist * pol
    return total


def compute_distance(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for n, dist, _ in graph.get_neighbors(path[i]):
            if n == path[i + 1]:
                total += dist
    return total


def _build_graph() -> Graph:
    """Build a Graph instance from the persisted graph store."""
    g = Graph()
    data = graph_store.get_graph()
    for node_id in data["cities"]:
        g.add_city(node_id)
    for road in data["roads"]:
        g.add_road(road["from"], road["to"], road["distance"], road["pollution"])
    return g


# =====================
# MAIN SERVICE
# =====================
def get_route_service(start: str, end: str):

    # GRAPH SETUP — loaded dynamically from data/graph.json
    g = _build_graph()

    # VALIDATION
    if start not in g.graph or end not in g.graph:
        return {"error": "Invalid start or end node"}

    # BASELINE ROUTE
    baseline = get_route(g, start, end)
    if baseline is None:
        return {"error": f"No path exists between '{start}' and '{end}'. Add roads to connect them."}
    shortest_path = baseline["path"]
    shortest_exposure = baseline["total_exposure"]

    # RL ENV ROUTE
    env = RLEnv(g, start=start, destination=end)

    state = env.reset()
    path = [state]

    done = False
    visited = set()
    steps = 0

    while not done:
        visited.add(state)

        neighbors = g.get_neighbors(state)
        neighbors = [(n, d, p) for (n, d, p) in neighbors if n not in visited]

        if not neighbors:
            break

        action = choose_best_neighbor(
            type("obj", (), {"total_exposure": 0}),
            neighbors,
            destination=end
        )

        next_state, reward, done = env.step(action)

        path.append(next_state)
        state = next_state

        steps += 1
        if steps > 20:
            break

    # FALLBACK (CRITICAL)
    if len(path) < 2 or path[-1] != end:
        eco_path = shortest_path
    else:
        eco_path = path

    # METRICS
    eco_exposure = compute_exposure(g, eco_path)
    eco_distance = compute_distance(g, eco_path)

    # IMPROVEMENT
    improvement_str = percent_improvement(shortest_exposure, eco_exposure)

    # RESPONSE
    return {
        "route": eco_path,
        "total_distance": eco_distance,
        "total_pollution": eco_exposure,
        "shortest_route": shortest_path,
        "shortest_exposure": shortest_exposure,
        "improvement": improvement_str
    }