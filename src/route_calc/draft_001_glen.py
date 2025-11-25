import heapq
import pandas as pd
import random
from pathlib import Path


def dijkstra(adj, src):
    nodes_length = len(adj)
    min_heap_priority_que = []
    distances_list = [float('inf')] * nodes_length
    parent = [-1] * nodes_length
    distances_list[src] = 0
    heapq.heappush(min_heap_priority_que, (0, src))

    while min_heap_priority_que:
        d, u = heapq.heappop(min_heap_priority_que)

        if d > distances_list[u]:
            continue

        for v, w in adj[u]:
            if distances_list[u] + w < distances_list[v]:
                distances_list[v] = distances_list[u] + w
                parent[v] = u
                heapq.heappush(min_heap_priority_que, (distances_list[v], v))

    return distances_list, parent


def get_path_names(parent, target_idx, idx_to_node_map):
    if parent[target_idx] == -1 and target_idx not in parent:
        return "No path found"

    path = []
    curr = target_idx
    while curr != -1:
        path.append(idx_to_node_map[curr])
        curr = parent[curr]

    return " -> ".join(path[::-1])


def create_graph(df, node_to_idx, is_rush_hour=False):
    num_nodes = len(node_to_idx)
    adj = [[] for _ in range(num_nodes)]
    risky_edge_indices = random.sample(range(len(df)), k=3)

    for index, row in df.iterrows():
        u = node_to_idx[row['start']]
        v = node_to_idx[row['end']]
        weight = row['duration']

        # Applying rush hour multiplier based on the scenario
        if is_rush_hour:
            multiplier = random.normalvariate(2, 0.5)
            multiplier = max(1, min(3, multiplier))
            weight = weight * multiplier

        # Applying extreme events; uncertainty
        if index in risky_edge_indices:
            if random.random() < 0.20:
                weight = weight * 10
                print(
                    f"Extreme event on the edge: {row['start']} <-> {row['end']}")
                print(f"Updated weight is: {weight:.2f} minutes")

        adj[u].append((v, weight))
        adj[v].append((u, weight))

    return adj


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    csv_path = script_dir.parent / "assets" / "routes.csv"

    try:
        df = pd.read_csv(csv_path)

        unique_nodes = sorted(list(set(df['start']) | set(df['end'])))
        node_to_idx = {name: i for i, name in enumerate(unique_nodes)}
        idx_to_node = {i: name for name, i in node_to_idx.items()}

        start_location = "Fenway Park"
        end_location = "Boston Tea Party Ships & Museum"
        src_idx = node_to_idx[start_location]
        target_idx = node_to_idx[end_location]

        print("Base case scenario:")

        base_adj = create_graph(df, node_to_idx, is_rush_hour=False)

        # A -> J
        dists, parents = dijkstra(base_adj, src_idx)
        print(f"\nDirection: {start_location} (A) -> {end_location} (J)")
        print(f"Shortest time: {dists[target_idx]:.2f} minutes")
        print(
            f"Shortest Path: {get_path_names(parents, target_idx, idx_to_node)}")

        # J -> A
        dists_rev, parents_rev = dijkstra(base_adj, target_idx)
        print(f"\nDirection: {end_location} (J) -> {start_location} (A)")
        print(f"Shortest time: {dists_rev[src_idx]:.2f} minutes")
        print(
            f"Shortest Path: {get_path_names(parents_rev, src_idx, idx_to_node)}")

        print("\nRush hour scenario:\n")

        rush_adj = create_graph(df, node_to_idx, is_rush_hour=True)

        # A -> J
        rh_dists, rh_parents = dijkstra(rush_adj, src_idx)
        print(f"\nDirection: {start_location} (A) -> {end_location} (J)")
        print(f"Shortest time: {rh_dists[target_idx]:.2f} minutes")
        print(
            f"Shortest Path: {get_path_names(rh_parents, target_idx, idx_to_node)}")

        # J -> A
        rh_dists_rev, rh_parents_rev = dijkstra(rush_adj, target_idx)
        print(f"\nDirection: {end_location} (J) -> {start_location} (A)")
        print(f"Shortest time: {rh_dists_rev[src_idx]:.2f} minutes")
        print(
            f"Shortest Path: {get_path_names(rh_parents_rev, src_idx, idx_to_node)}")

    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_path}")
    except KeyError as e:
        print(f"Error: Node name not found in dataset: {e}")
