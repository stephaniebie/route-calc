import heapq
import pandas as pd
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


def get_path_names(parent, target_idx, ending_node):
    path = []
    curr = target_idx
    while curr != -1:
        path.append(ending_node[curr])
        curr = parent[curr]
    return " -> ".join(path[::-1])


script_dir = Path(__file__).parent
csv_path = script_dir.parent / "assets" / "routes.csv"
df = pd.read_csv(csv_path)

unique_nodes = sorted(list(set(df['start']) | set(df['end'])))
starting_node = {name: i for i, name in enumerate(unique_nodes)}
ending_node = {i: name for name, i in starting_node.items()}

length_of_unique_nodes = len(unique_nodes)
adj = [[] for _ in range(length_of_unique_nodes)]

for _, row in df.iterrows():
    u = starting_node[row['start']]
    v = starting_node[row['end']]
    w = row['duration']

    adj[u].append((v, w))
    adj[v].append((u, w))

start_location = "Fenway Park"
end_location = "Boston Tea Party Ships & Museum"

starting_index = starting_node[start_location]
ending_index = starting_node[end_location]

distances, parents = dijkstra(adj, starting_index)


print("just the best case scenario")
print(f"From:{start_location}")
print(f"To:{end_location}")
print("-" * 30)
print(f"Shortest Time: {distances[ending_index]} minutes")
print(f"Optimal Route: {get_path_names(parents, ending_index, ending_node)}")

if __name__ == "__main__":
    test_adj = [[(1, 4), (2, 1)], [(2, 2)], []]

    source_node = 0
    dijkstra(test_adj, source_node)
