# we will use the adjacency list and implement Dijkstra's algorithm considering different traffic scenarios:
# 1. Base Case: Average Traffic Conditions
# 2. Rush Hour Scenario: High Traffic Conditions
# to obtain the rush hour scenario, apply the multiplier to the weights, using a normal distribution with mean = 2 and standard deviation = 0.5.
# apply the multiplier to each edge weight in the graph to simulate rush hour conditions.
# Map.py
import math
import random
import heapq
from Route import load_adjacencylist_from_csv


def rush_hour_graph(base_graph, mean=2.0, std=0.5):

    # returns a new graph where each edge weight is multiplied by a random factor with the above mean and sd from normal distribution.
    # need to also ensure the graph stays undirected with the effected weights.
    rush_graph = {}
    # Cache to store the multiplier for each undirected edge
    edge_multipliers = {}

    for u, edges in base_graph.items():
        rush_graph[u] = []
        for v, w in edges:
            # Create a canonical edge representation (undirected)
            edge_key = tuple(sorted((u, v)))

            # If we haven't seen this edge before, we geneate a multiplier
            if edge_key not in edge_multipliers:
                factor = random.normalvariate(mean, std)
                # make sure the factor is between ranges 1-3
                factor = max(1.0, min(3.0, factor))
                edge_multipliers[edge_key] = factor
            else:
                factor = edge_multipliers[edge_key]

            
            new_w = w * factor
            rush_graph[u].append((v, new_w))

    return rush_graph

def dijkstra_shortest_path(graph, source):
    """
    Standard Dijkstra using adjacency list:
    graph[node] = [(neighbor, weight), ...]
    Returns:
    dist: dict of node -> distance from source
    prev: dict of node -> previous node in shortest path
    """
    dist = {node: math.inf for node in graph}
    dist[source] = 0.0
    prev = {node: None for node in graph}

    pq = [(0.0, source)] 

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def build_the_path(prev, start, end):
    #reconstructs path from start to end using prev dictionary.
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if path and path[0] == start:
        return path
    return []
