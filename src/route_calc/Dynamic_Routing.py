# handles the Uncertainty and Unexpected Events (dynamic solution) over the map
# atleast 3 pairs of nodes must have extreme events such as 
#route blockage,severe delays (10x or more)
#model the above using discrete distributions such that 80% chance no disruption and 20% of major disruption, use random module to simulate
# implement Dijkstra's algorithm to find the optimal path considering these dynamic disruptions

# use the visualize.py module to visualize the dynamic routing results
# Dynamic_Routing.py
import random

def sample_event_edges(graph, num_events=3):
    #using set to capture unique undirected edges
    edges = set()
    for u in graph:
        for v, _ in graph[u]:
            edge = tuple(sorted((u, v)))
            edges.add(edge)
    edges = list(edges)
    return random.sample(edges, num_events)

def uncertain_events_on_edges(graph, event_edges):
    new_graph = {u: [] for u in graph}
    # Assign scenarios: one delay, two blockages; each with 20% chance per run
    for u in graph:
        for v, w in graph[u]:
            edge = tuple(sorted((u, v)))
            # Severe delay (10x) for the first edge, if its an event edge
            if edge == event_edges[0]:
                if random.random() < 0.2:
                    print(f"Severe delay on edge {edge}")
                    w = w * 10
            # road blockages for the other 2 event edges, which means we skip adding them to the graph
            if edge == event_edges[1] or edge == event_edges[2]:
                print(f"Road blockage on edge {edge}")
                if random.random() < 0.2:
                    continue  # skipping this edge as a blockage
            new_graph[u].append((v, w))
    return new_graph
