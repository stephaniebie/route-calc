#creating the adjacency list for the map from the CSV file
# route.py
import csv

def load_adjacencylist_from_csv(filename):
    #returns graph[node] = [(neighbor, duration), ...]
    graph = {}
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["start"]
            v = row["end"]
            w = float(row["duration"])

            # Add BOTH directions
            graph.setdefault(u, []).append((v, w))
            graph.setdefault(v, []).append((u, w))

    return graph